from collections import defaultdict
from datetime import datetime

import psycopg2
from sqlalchemy import text


def get_mandates(db, representee_identifier=None, delegate_identifier=None, subdelegated_by_identifier=None):
    params = {
        'date_now': datetime.today()
    }
    where_conditions = [
        "(validity_period_through is NULL OR validity_period_through >= :date_now)"
    ]
    if representee_identifier:
        where_conditions.append("representee_identifier=:representee_id")
        params['representee_id'] = representee_identifier

    if delegate_identifier:
        where_conditions.append('delegate_identifier=:delegate_identifier')
        params['delegate_identifier'] = delegate_identifier

    if subdelegated_by_identifier:
        where_conditions.append("original_mandate_id IS NOT NULL")
        where_conditions.append("created_by_represented_person=:subdelegate_identifier")
        params['subdelegate_identifier'] = subdelegated_by_identifier

    sql = f"SELECT * FROM representee_mandates_view WHERE {' AND '.join(where_conditions)}"
    result = db.session.execute(text(sql), params)
    rows = result.fetchall()
    return [dict(row._mapping) for row in rows]

def extract_representee_mandates(data):
    grouped = defaultdict(lambda: {
        'representee_type': None,
        'representee_id': None,
        'representee_first_name': None,
        'representee_surname': None,
        'representee_legal_name': None,
        'representee_identifier': None,
        'delegates': defaultdict(lambda: {
            'delegate_type': None,
            'delegate_id': None,
            'delegate_first_name': None,
            'delegate_surname': None,
            'delegate_legal_name': None,
            'delegate_identifier': None,
            'mandates': []
        })
    })

    for entry in data:
        grouped[entry['representee_identifier']]['representee_type'] = entry['representee_type']
        grouped[entry['representee_identifier']]['representee_id'] = entry['representee_id']
        grouped[entry['representee_identifier']]['representee_first_name'] = entry['representee_first_name']
        grouped[entry['representee_identifier']]['representee_surname'] = entry['representee_surname']
        grouped[entry['representee_identifier']]['representee_legal_name'] = entry['representee_legal_name']
        grouped[entry['representee_identifier']]['representee_identifier'] = entry['representee_identifier']

        delegate = grouped[entry['representee_identifier']]['delegates'][entry['delegate_identifier']]
        delegate['delegate_type'] = entry['delegate_type']
        delegate['delegate_id'] = entry['delegate_id']
        delegate['delegate_first_name'] = entry['delegate_first_name']
        delegate['delegate_surname'] = entry['delegate_surname']
        delegate['delegate_legal_name'] = entry['delegate_legal_name']
        delegate['delegate_identifier'] = entry['delegate_identifier']

        delegate['mandates'].append({
            'mandate_id': entry['mandate_id'],
            'role': entry['role'],
            'validity_period_from': entry['validity_period_from'],
            'validity_period_through': entry['validity_period_through'],
            'can_sub_delegate': entry['can_sub_delegate'],
            'created_by': entry['created_by'],
            'created_by_represented_person': entry['created_by_represented_person'],
            'original_mandate_id': entry['original_mandate_id'],
            'document_uuid': entry['document_uuid'],
            'can_display_document_to_delegate': entry['can_display_document_to_delegate'],
            'link_delete': entry['link_delete'],
            'link_add_sub_delegate': entry['link_add_sub_delegate']
        })

    representee = dict(grouped[next(iter(grouped))])
    delegates = list(representee.pop('delegates').values())
    return representee, delegates


def extract_delegates_mandates(data):
    grouped = defaultdict(lambda: {
        'delegate_type': None,
        'delegate_id': None,
        'delegate_first_name': None,
        'delegate_surname': None,
        'delegate_legal_name': None,
        'delegate_identifier': None,
        'representees': defaultdict(lambda: {
            'representee_type': None,
            'representee_id': None,
            'representee_first_name': None,
            'representee_surname': None,
            'representee_legal_name': None,
            'representee_identifier': None,
            'mandates': []
        })
    })

    for entry in data:
        grouped[entry['delegate_identifier']]['delegate_type'] = entry['delegate_type']
        grouped[entry['delegate_identifier']]['delegate_id'] = entry['delegate_id']
        grouped[entry['delegate_identifier']]['delegate_first_name'] = entry['delegate_first_name']
        grouped[entry['delegate_identifier']]['delegate_surname'] = entry['delegate_surname']
        grouped[entry['delegate_identifier']]['delegate_legal_name'] = entry['delegate_legal_name']
        grouped[entry['delegate_identifier']]['delegate_identifier'] = entry['delegate_identifier']

        representee = grouped[entry['delegate_identifier']]['representees'][entry['representee_identifier']]
        representee['representee_type'] = entry['representee_type']
        representee['representee_id'] = entry['representee_id']
        representee['representee_first_name'] = entry['representee_first_name']
        representee['representee_surname'] = entry['representee_surname']
        representee['representee_legal_name'] = entry['representee_legal_name']
        representee['representee_identifier'] = entry['representee_identifier']

        representee['mandates'].append({
            'mandate_id': entry['mandate_id'],
            'role': entry['role'],
            'validity_period_from': entry['validity_period_from'],
            'validity_period_through': entry['validity_period_through'],
            'can_sub_delegate': entry['can_sub_delegate'],
            'created_by': entry['created_by'],
            'created_by_represented_person': entry['created_by_represented_person'],
            'original_mandate_id': entry['original_mandate_id'],
            'document_uuid': entry['document_uuid'],
            'can_display_document_to_delegate': entry['can_display_document_to_delegate'],
            'link_delete': entry['link_delete'],
            'link_add_sub_delegate': entry['link_add_sub_delegate']
        })

    delegate = dict(grouped[next(iter(grouped))])
    representees = list(delegate.pop('representees').values())
    return delegate, representees


def extract_mandate_data(payload):
    data = {
        'delegate_first_name': None,
        'delegate_first_name': None,
        'delegate_surname': None,
        'delegate_type': None,
        'representee_identifier': None,
        'representee_legal_name': None,
        'representee_type': None,
        'mandate_role': None,
        'mandate_validity_period_from': None,
        'mandate_validity_period_through': None,
        'mandate_can_sub_delegate': False,
        'data_created_by': None,
        'data_created_by_represented_person': None,
        'data_original_mandate_id': None,
        'document_uuid': None,
        'data_can_display_document_to_delegate': False,
    }

    delegate = payload['delegate']
    representee = payload['representee']
    mandate = payload.get('mandate', {})
    data_ = payload.get('data', {})
    document = payload.get('document', {})

    data['delegate_first_name'] = delegate.get('firstName')
    data['delegate_identifier'] = delegate['identifier']
    data['delegate_surname'] = delegate.get('surname')
    data['delegate_type'] = delegate['type']

    data['representee_identifier'] = representee['identifier']
    data['representee_legal_name'] = representee.get('legalName')
    data['representee_type'] = representee['type']

    data['mandate_role'] = mandate.get('role')
    validity_period = mandate.get('validityPeriod', {})
    data['mandate_validity_period_from'] = validity_period.get('from')
    data['mandate_validity_period_through'] = validity_period.get('through')
    data['mandate_can_sub_delegate'] = mandate.get('canSubDelegate')

    data['data_created_by'] = data_.get('createdBy', '')
    data['data_created_by_represented_person'] = data_.get('createdByRepresentedPerson')
    data['data_original_mandate_id'] = data_.get('originalMandateId')
    data['document_uuid'] = document.get('uuid')
    if document.get('singleDelegate') and document.get('uuid'):
        data['data_can_display_document_to_delegate'] = True

    return data


def extract_mandate_subdelegate_data(payload):
    data = {
        'sub_delegate_first_name': None,
        'sub_delegate_surname': None,
        'sub_delegate_type': None,
        'sub_delegate_identifier': None,
        'representee_identifier': None,
        'delegate_identifier': None,
        'mandate_identifier': None,
        'sub_mandate_validity_period_from': None,
        'sub_mandate_validity_period_through': None,
        'data_created_by': None,
        'data_created_by_represented_person': None,
        'document_uuid': None,
        'data_can_display_document_to_delegate': False,
    }

    sub_delegate = payload.get('subDelegate')
    validity_period = payload.get('validityPeriod', {})
    document = payload.get('document', {})

    data['sub_delegate_first_name'] = sub_delegate.get('firstName')
    data['sub_delegate_identifier'] = sub_delegate['identifier']
    data['sub_delegate_surname'] = sub_delegate.get('surname')
    data['sub_delegate_type'] = sub_delegate['type']

    data['sub_mandate_validity_period_from'] = validity_period.get('from')
    data['sub_mandate_validity_period_through'] = validity_period.get('through')
    data['document_uuid'] = document.get('uuid')
    if document.get('singleDelegate') and document.get('uuid'):
        data['data_can_display_document_to_delegate'] = True
    return data


def create_mandate_pg(uri, data):
    conn = psycopg2.connect(uri)
    conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)

    cur = conn.cursor()
    cur.callproc(
        'function_create_mandate', [
            data['delegate_first_name'],
            data['delegate_identifier'],
            data['delegate_surname'],
            data['delegate_type'],
            data['representee_identifier'],
            data['representee_legal_name'],
            data['representee_type'],
            data['mandate_role'],
            data['mandate_validity_period_from'],
            data['mandate_validity_period_through'],
            data['mandate_can_sub_delegate'],
            data['data_created_by'],
            data['data_created_by_represented_person'],
            data['data_original_mandate_id'],
            data['document_uuid'],
            data['data_can_display_document_to_delegate']
        ]
    )
    cur.close()
    conn.close()


def delete_mandate_pg(uri, representee_identifier,
                      delegate_identifier, mandate_identifier):
    conn = psycopg2.connect(uri)
    conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)

    cur = conn.cursor()
    cur.callproc(
        'function_delete_mandate', [
            representee_identifier,
            delegate_identifier,
            mandate_identifier,
        ]
    )
    result = cur.fetchone()[0]
    cur.close()
    conn.close()
    return result


def subdelegate_mandate_pg(uri, data):
    conn = psycopg2.connect(uri)
    conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)
    cur = conn.cursor()
    cur.callproc(
        'function_insert_mandate_subdelegate', [
            data['sub_delegate_first_name'],
            data['sub_delegate_surname'],
            data['sub_delegate_type'],
            data['sub_delegate_identifier'],
            data['representee_identifier'],
            data['delegate_identifier'],
            data['mandate_identifier'],
            data['sub_mandate_validity_period_from'],
            data['sub_mandate_validity_period_through'],
            data['data_created_by'],
            data['data_created_by_represented_person'],
            data['document_uuid'],
            data['data_can_display_document_to_delegate'],
        ]
    )
    result = cur.fetchone()[0]
    cur.close()
    conn.close()
    return result


def get_roles_pg(db):
    sql = "SELECT * FROM roles_view"
    result = db.session.execute(text(sql))
    rows = result.fetchall()
    return [dict(row._mapping) for row in rows]
