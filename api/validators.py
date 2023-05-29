import re

from cerberus import Validator

from api.exceptions import (CompanyCodeInvalid, MandateDataInvalid,
                            MandateSubdelegateDataInvalid)
add_mandate_subdelegate_schema = {
    "authorizations": {
        "type": "list",
        "schema": {
            "type": "dict",
            "schema": {
                "hasRole": {"type": "string", "empty": False},
                "userIdentifier": {"type": "string", "empty": False}
            }
        },
        "default": []
    },
    "document": {
        "type": "dict",
        "schema": {
            "singleDelegate": {"type": "boolean"},
            "uuid": {"type": "string", "empty": False}
        }
    },
    "subDelegate": {
        "type": "dict",
        "schema": {
            "firstName": {"type": "string"},
            "identifier": {"type": "string", "required": True},
            "surname": {"type": "string"},
            "type": {"type": "string", "required": True},
        }
    },
    "validityPeriod": {
        "type": "dict",
        "schema": {
            "from": {"type": "string"},
            "through": {"type": "string"}
        }
    }
}

add_mandate_triplet_schema = {
        "delegate": {
            "type": "dict",
            "required": True,
            "schema": {
                "firstName": {"type": "string", "required": False},
                "identifier": {"type": "string", "required": True},
                "surname": {"type": "string", "required": False},
                "type": {"type": "string", "required": True},
            },
        },
        "representee": {
            "type": "dict",
            "required": True,
            "schema": {
                "identifier": {"type": "string", "required": True},
                "legalName": {"type": "string", "required": False},
                "type": {"type": "string", "required": True},
            },
        },
        "document": {
            "type": "dict",
            "required": False,
            "schema": {
                "singleDelegate": {"type": "boolean", "required": False},
                "uuid": {"type": "string", "required": False},
            },
        },
        "mandate": {
            "type": "dict",
            "required": False,
            "schema": {
                "canSubDelegate": {"type": "boolean", "required": False},
                "role": {"type": "string", "required": True},
                "validityPeriod": {
                    "type": "dict",
                    "required": False,
                    "schema": {
                        "from": {"type": "string", "required": False},
                        "through": {"type": "string", "required": False},
                    },
                },
            },
        },
        "authorizations": {
            "type": "list",
            "required": False,
            "schema": {
                "type": "dict",
                "schema": {
                    "hasRole": {"type": "string", "required": True},
                    "userIdentifier": {"type": "string", "required": True},
                },
            },
        },
    }


def validate_person_company_code(code: str, error_config) -> None:
    if not code:
        return
    pattern = r'^[A-Z]{2}[A-Za-z0-9_\-\.~]{1,253}$'
    if not re.match(pattern, code):
        raise CompanyCodeInvalid('Legal person validation failed', error_config)


def validate_add_mandate_payload(payload, error_config, representee_identifier, delegate_identifier):
    v = Validator()
    if not v.validate(payload, add_mandate_triplet_schema):
        raise MandateDataInvalid('Add Mandate Triplet data is invalid', error_config)
    if representee_identifier != payload['representee']['identifier']:
        raise MandateDataInvalid('Representee does not match', error_config)
    if delegate_identifier != payload['delegate']['identifier']:
        raise MandateDataInvalid('Delegate does not match', error_config)


def validate_add_mandate_subdelegate_payload(payload, error_config):
    v = Validator()
    if not v.validate(payload, add_mandate_subdelegate_schema):
        raise MandateSubdelegateDataInvalid('Add Mandate Subdelegate data is invalid', error_config)