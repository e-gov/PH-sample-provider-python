import os

import psycopg2
import yaml
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_swagger_ui import get_swaggerui_blueprint
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import sessionmaker

from api.enums import is_valid_action
from api.exceptions import (CompanyCodeInvalid,
                            ErrorConfigBase, MandateDataInvalid,
                            MandateNotFound, MandateSubdelegateDataInvalid,
                            UnprocessableRequestError, ActionInvalid)
from api.serializers import (serialize_delegate_mandates,
                             serialize_representee_mandates, serialize_deleted_subdelegated_mandates)
from api.services import (create_mandate_pg, delete_mandate_pg,
                          extract_delegates_mandates, extract_mandate_data,
                          extract_mandate_subdelegate_data,
                          extract_representee_mandates, get_mandates,
                          get_roles_pg, subdelegate_mandate_pg, delete_subdelegated_mandates_pg, get_person_pg,
                          get_deleted_mandates)
from api.validators import (validate_add_mandate_payload,
                            validate_add_mandate_subdelegate_payload,
                            validate_person_company_code)

db = SQLAlchemy()


def create_error_handler(status_code):
    def error_handler(e):
        return jsonify(e.to_dict()), status_code

    return error_handler


def parse_settings(filename):
    with open(os.path.join(os.path.dirname(__file__), filename), 'r') as stream:
        return yaml.safe_load(stream)


def create_app():
    app = Flask(__name__)
    app.config.from_envvar('APP_SETTINGS')
    db.init_app(app)
    app.config['SETTINGS'] = parse_settings(app.config['SETTINGS_PATH'])

    SWAGGER_URL = "/v1/api-docs"
    API_URL = "/static/x-road-services-consumed-by-paasuke.json"
    SWAGGER_BLUEPRINT = get_swaggerui_blueprint(
        SWAGGER_URL,
        API_URL,
        config={
            'app_name': "X-road services consumed by Pääsuke"
        }
    )
    app.register_blueprint(SWAGGER_BLUEPRINT, url_prefix=SWAGGER_URL)

    app.errorhandler(ActionInvalid)(create_error_handler(501))
    app.errorhandler(CompanyCodeInvalid)(create_error_handler(400))
    app.errorhandler(MandateDataInvalid)(create_error_handler(400))
    app.errorhandler(MandateSubdelegateDataInvalid)(create_error_handler(400))
    app.errorhandler(MandateNotFound)(create_error_handler(404))
    app.errorhandler(UnprocessableRequestError)(create_error_handler(422))

    def make_success_response(response_data, status_code):
        response = jsonify(response_data)
        response.status_code = status_code
        if app.config['ALLOW_ANY_ORIGIN']:
            response.headers['Access-Control-Allow-Origin'] = '*'
        return response

    @app.errorhandler(Exception)
    def handle_unhandled_error(e):
        error_config = app.config['SETTINGS']['errors']['internal_server_error']
        base = ErrorConfigBase(
            'Internal server error. Please try again later.',
            error_config,
            500
        )
        app.logger.exception('Unexpected error occurred: %s', e)
        return jsonify(base.to_dict()), 500

    @app.route('/v1/delegates/<string:delegate_identifier>/representees/mandates', methods=['GET'])
    def get_delegates_representees_mandates(delegate_identifier):
        xroad_user_id = request.headers.get('X-Road-UserId')
        app.logger.info(f'X-Road-UserId: {xroad_user_id} Getting delegate mandates')
        error_config = app.config['SETTINGS']['errors']['legal_person_format_validation_failed']
        validate_person_company_code(delegate_identifier, error_config)

        data_rows = get_mandates(db, delegate_identifier=delegate_identifier)
        if not data_rows:
            return make_success_response(data_rows, 200)
        delegate, representees = extract_delegates_mandates(data_rows)
        response_data = serialize_delegate_mandates(delegate, representees, app.config['SETTINGS'])
        return make_success_response(response_data, 200)

    @app.route('/v1/representees/<string:representee_identifier>/delegates/mandates', methods=['GET'])
    def get_representees_delegates_mandates(representee_identifier):
        xroad_user_id = request.headers.get('X-Road-UserId')
        app.logger.info(f'X-Road-UserId: {xroad_user_id} Getting representee mandates')

        args = request.args
        subdelegated_by_identifier = args.get('subDelegatedBy')
        delegate_identifier = args.get('delegate')

        error_config = app.config['SETTINGS']['errors']['legal_person_format_validation_failed']
        [
            validate_person_company_code(code, error_config)
            for code in [representee_identifier, delegate_identifier, subdelegated_by_identifier]
        ]
        data_rows = get_mandates(
            db,
            representee_identifier=representee_identifier,
            delegate_identifier=delegate_identifier,
            subdelegated_by_identifier=subdelegated_by_identifier
        )
        if not data_rows:
            return make_success_response(data_rows, 200)

        representee, delegates = extract_representee_mandates(data_rows)
        response_data = serialize_representee_mandates(representee, delegates, app.config['SETTINGS'])
        return make_success_response(response_data, 200)

    @app.route('/v1/representees/<string:representee_identifier>/delegates/<string:delegate_identifier>/mandates',
               methods=['POST'])
    def post_representee_delegate_mandate(representee_identifier, delegate_identifier):
        xroad_user_id = request.headers.get('X-Road-UserId')
        app.logger.info(f'X-Road-UserId: {xroad_user_id} is about to add a mandate')

        error_config = app.config['SETTINGS']['errors']['legal_person_format_validation_failed']
        [
            validate_person_company_code(code, error_config)
            for code in [representee_identifier, delegate_identifier]
        ]
        data = request.json
        error_config = app.config['SETTINGS']['errors']['mandate_data_invalid']
        validate_add_mandate_payload(data, error_config, representee_identifier, delegate_identifier)

        data_to_insert = extract_mandate_data(data)
        data_to_insert['data_created_by'] = xroad_user_id
        db_uri = app.config['SQLALCHEMY_DATABASE_URI']
        try:
            create_mandate_pg(db_uri, data_to_insert)
        except psycopg2.errors.RaiseException as e:
            app.logger.exception(str(e))
            error_config = app.config['SETTINGS']['errors']['unprocessable_request']
            raise UnprocessableRequestError(
                'Unprocessable request while creating mandate. Something went wrong.',
                error_config
            )
        return make_success_response([], 201)

    @app.route(
        '/v1/representees/<string:representee_id>/delegates/<string:delegate_id>/mandates/<string:mandate_id>',
        methods=['PUT']
    )
    def delete_mandate(representee_id, delegate_id, mandate_id):
        xroad_user_id = request.headers.get('X-Road-UserId')
        app.logger.info(f'X-Road-UserId: {xroad_user_id} Deleting mandate')

        data = request.json
        if data.get('action') is None or not is_valid_action(data['action']):
            error_config = app.config['SETTINGS']['errors']['action_invalid']
            raise ActionInvalid("Action invalid", error_config)

        db_uri = app.config['SQLALCHEMY_DATABASE_URI']
        engine = create_engine(db_uri)
        Session = sessionmaker(bind=engine)
        session = Session()
        try:
            with session.begin():
                conn = session.connection().connection
                data_rows_deleted_subdelegated_mandates = delete_subdelegated_mandates_pg(conn, mandate_id)
                data_row_deleted_mandate = delete_mandate_pg(
                    conn,
                    representee_id,
                    delegate_id,
                    mandate_id
                )

                if data_row_deleted_mandate:
                    data_rows_mandates = get_mandates(db) # because the changes related to mandates are not persisted yet (running in session, we have to search from active mandates)
                    response_data = serialize_deleted_subdelegated_mandates(
                        data_rows_deleted_subdelegated_mandates,
                        data_rows_mandates,
                        app.config['SETTINGS']
                    )
                    return make_success_response(response_data, 200)
        except Exception as custom_exception:
            session.rollback()
            app.logger.exception(str(custom_exception))
            error_config = app.config['SETTINGS']['errors']['unprocessable_request']
            raise UnprocessableRequestError(str(custom_exception), error_config)
        finally:
            session.close()

        error_config = app.config['SETTINGS']['errors']['mandate_not_found']
        raise MandateNotFound('Mandate to delete was not found', error_config)

    @app.route(
        '/v1/representees/<string:representee_id>/delegates/<string:delegate_id>/mandates/<string:mandate_id>/subdelegates',
        methods=['POST']
    )
    def post_subdelegate_mandate(representee_id, delegate_id, mandate_id):
        xroad_user_id = request.headers.get('X-Road-UserId')
        xroad_represented_party = request.headers.get('X-Road-Represented-Party')
        app.logger.info(f'X-Road-UserId: {xroad_user_id} Creating subdelegate')

        data = request.json
        error_config = app.config['SETTINGS']['errors']['mandate_subdelegate_data_invalid']
        validate_add_mandate_subdelegate_payload(data, error_config)
        if data.get('subDelegate'):
            error_config = app.config['SETTINGS']['errors']['legal_person_format_validation_failed']
            validate_person_company_code(data['subDelegate']['identifier'], error_config)
        data_to_insert = extract_mandate_subdelegate_data(data)

        data_to_insert['representee_id'] = representee_id
        data_to_insert['delegate_id'] = delegate_id
        data_to_insert['mandate_id'] = mandate_id

        data_to_insert['data_created_by'] = xroad_user_id
        try:
            result = subdelegate_mandate_pg(app.config['SQLALCHEMY_DATABASE_URI'], data_to_insert)
        except psycopg2.errors.RaiseException as e:
            app.logger.exception(str(e))
            error_config = app.config['SETTINGS']['errors']['unprocessable_request']
            raise UnprocessableRequestError(
                'Unprocessable request while subdelegating mandate. Something went wrong.',
                error_config
            )
        if not result:
            error_config = app.config['SETTINGS']['errors']['mandate_not_found']
            raise MandateNotFound('Mandate to delete was not found', error_config)
        return make_success_response([], 200)

    @app.route('/v1/roles', methods=['GET'])
    def get_roles():
        roles = []
        roles_data = get_roles_pg(db)
        mapped = {
            'code': 'code',
            'delegate_can_equal_to_representee': 'delegateCanEqualToRepresentee',
            'modified': 'modified',
            'validity_period_from_not_in_future': 'validityPeriodFromNotInFuture',
            'validity_period_through_must_be_undefined': 'validityPeriodThroughMustBeUndefined',
            'assignable_only_if_representee_has_role_in': 'assignableOnlyIfRepresenteeHasRoleIn',
            'delegate_type': 'delegateType',
            'can_sub_delegate': 'canSubDelegate',
            'addable_by': 'addableBy',
            'adding_must_be_signed': 'addingMustBeSigned',
            'assignable_by': 'assignableBy',
            'waivable_by': 'waivableBy',
            'waiving_must_be_signed': 'waivingMustBeSigned',
            'withdrawable_by': 'withdrawableBy',
            'withdrawal_must_be_signed': 'withdrawalMustBeSigned',
            'deletable_by': 'deletableBy',
            'deletable_by_delegate': 'deletableByDelegate',
            'representee_type': 'representeeType',
            'visible': 'visible',
        }
        for role in roles_data:
            role_item = {
                mapped[key]: value
                for key, value in role.items()
                if (value is not None and (type(value) != list or type(value) == list and value) and key in mapped)
            }
            role_item['title'] = {
                'en': role['title_en'],
                'et': role['title_et'],
                'ru': role['title_ru']
            }
            role_item['description'] = {
                'en': role['description_en'],
                'et': role['description_et'],
                'ru': role['description_ru']
            }
            if role_item.get('modified'):
                role_item['modified'] = role_item['modified'].isoformat()
            roles.append(role_item)

        return make_success_response(roles, 200)

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(
        debug=app.config.get('DEBUG'),
        host=app.config.get('HOST', '0.0.0.0'),
        port=app.config.get('PORT', 8082)
    )
