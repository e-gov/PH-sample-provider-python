import pytest

from api.app import create_app


@pytest.fixture()
def app():
    app = create_app()
    app.config.update({
        'TESTING': True,
    })
    yield app


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def config(app):
    return app.config


def test_delegate_format_validation_failed(client, config):
    response = client.get('/v1/delegates/1EE1234567/representees/mandates')
    assert response.status_code == 400
    error_config = config['SETTINGS']['errors']['legal_person_format_validation_failed']

    assert response.json == {
        'href': error_config['reference'],
        'title': 'Legal person validation failed',
        'translation': error_config['translation'],
        'type': error_config['type']
    }


def test_delegate_not_found_empty_list(client, config):
    response = client.get('/v1/delegates/EE3333333/representees/mandates')
    assert response.status_code == 200
    assert response.json == []


def test_delegate_mandates(client):
    response = client.get('/v1/delegates/EE22202222222/representees/mandates')
    assert response.status_code == 200
    assert response.json == [
        {
            'delegate': {
                'firstName': 'EE First Name',
                'identifier': 'EE22202222222',
                'surname': 'EE Surname 2',
                'type': 'NATURAL_PERSON'
            },
            'mandates': [
                {
                    'links': {
                        'delete': '/v1/representees/100001/delegates/100002/mandates/150001',
                        'origin': 'https://example.com/mandate/150001'
                    },
                    'role': 'AGENCY_X:ENTER',
                    'subDelegable': False
                }
            ],
            'representee': {
                'identifier': 'EE11111111',
                'legalName': 'EE Legal Person 1',
                'type': 'LEGAL_PERSON'
            }
        }
    ]


def test_representee_format_validation_failed(client, config):
    response = client.get('/v1/representees/1EE33333333/delegates/mandates')
    assert response.status_code == 400
    error_config = config['SETTINGS']['errors']['legal_person_format_validation_failed']

    assert response.json == {
        'href': error_config['reference'],
        'title': 'Legal person validation failed',
        'translation': error_config['translation'],
        'type': error_config['type']
    }


def test_representee_not_found_empty_list(client, config):
    response = client.get('/v1/representees/EE4q486846/delegates/mandates')
    assert response.status_code == 200
    assert response.json == []


@pytest.mark.parametrize('query_param', [
    {
        'delegate': 'not-valid'
    },
    {
        'subDelegatedBy': 'not-valid'
    }
])
def test_company_format_validation_failed(client, query_param, config):
    response = client.get(
        'v1/representees/EE33333333/delegates/mandates',
        query_string=query_param
    )
    assert response.status_code == 400
    error_config = config['SETTINGS']['errors']['legal_person_format_validation_failed']

    assert response.json == {
        'href': error_config['reference'],
        'title': 'Legal person validation failed',
        'translation': error_config['translation'],
        'type': error_config['type']
    }


def test_representee_mandates(client):
    response = client.get('v1/representees/EE11111111/delegates/mandates')
    assert response.status_code == 200
    assert response.json == [
        {
            'delegate': {
                'firstName': 'EE First Name',
                'identifier': 'EE22202222222',
                'surname': 'EE Surname 2',
                'type': 'NATURAL_PERSON'
            },
            'mandates': [
                {
                    'links': {
                        'delete': '/v1/representees/100001/delegates/100002/mandates/150001',
                        'origin': 'https://example.com/mandate/150001'
                    },
                    'role': 'AGENCY_X:ENTER',
                    'subDelegable': False
                }
            ],
            'representee': {
                'identifier': 'EE11111111',
                'legalName': 'EE Legal Person 1',
                'type': 'LEGAL_PERSON'
            }
        },
        {
            'delegate': {
                'firstName': 'LT First',
                'identifier': 'LT33303333333',
                'surname': 'LT Surname 2',
                'type': 'NATURAL_PERSON'
            },
            'mandates': [
                {
                    'links': {
                        'delete': '/v1/representees/100001/delegates/100003/mandates/150002',
                        'origin': 'https://example.com/mandate/150002'
                    },
                    'role': 'AGENCY_X:ENTER_AND_SUBMIT',
                    'subDelegable': False,
                    'validityPeriod': {'from': '2021-01-01'}
                }
            ],
            'representee': {
                'identifier': 'EE11111111',
                'legalName': 'EE Legal Person 1',
                'type': 'LEGAL_PERSON'
            }
        }
    ]


def test_representee_mandates_filter_by_delegate(client):
    response = client.get(
        'v1/representees/EE11111111/delegates/mandates',
        query_string={'delegate': 'EE22202222222'}
    )
    assert response.status_code == 200
    assert response.json == [
        {
            'delegate': {
                'firstName': 'EE First Name',
                'identifier': 'EE22202222222',
                'surname': 'EE Surname 2',
                'type': 'NATURAL_PERSON'
            },
            'mandates': [
                {
                    'links': {
                        'delete': '/v1/representees/100001/delegates/100002/mandates/150001',
                        'origin': 'https://example.com/mandate/150001'
                    },
                    'role': 'AGENCY_X:ENTER',
                    'subDelegable': False
                }
            ],
            'representee': {
                'identifier': 'EE11111111',
                'legalName': 'EE Legal Person 1',
                'type': 'LEGAL_PERSON'
            }
        }
    ]


def test_representee_mandates_filter_by_sub_delegated_by(client):
    response = client.get(
        'v1/representees/EE44444444/delegates/mandates',
        query_string={'subDelegatedBy': 'EE55555555'}
    )
    assert response.status_code == 200
    assert response.json == [
        {
            'delegate': {
                'firstName': 'EE First Name',
                'identifier': 'EE60606666666',
                'surname': 'EE Surname 6',
                'type': 'NATURAL_PERSON'
            },
            'mandates': [
                {
                    'links': {
                        'delete': '/v1/representees/100004/delegates/100006/mandates/150004'
                    },
                    'role': 'AGENCY_X:MANDATES_MANAGER',
                    'subDelegable': False,
                    'subDelegatorIdentifier': 'EE55555555',
                    'validityPeriod': {
                        'from': '2020-01-01',
                        'through': '2030-12-31'
                    }
                }
            ],
            'representee': {
                'identifier': 'EE44444444',
                'legalName': 'EE Legal Person 4',
                'type': 'LEGAL_PERSON'
            }
        }
    ]


def test_sub_delegate_deleted_mandate(client):
    body = {
        "subDelegate": {
            "type": "NATURAL_PERSON",
            "firstName": "LT First",
            "surname": "LT Surname 2",
            "identifier": "LT33303333333"
        },
        "validityPeriod": {
            "from": "2028-01-01",
            "through": "2030-12-31"
        },
        "authorizations": [
            {
                "userIdentifier": "EE39912310123",
                "hasRole": "BR_REPRIGHT:SOLEREP"
            }
        ],
        "document": {
            "uuid": "5b72e01c-fa7f-479c-b014-cc19efe5b732",
            "singleDelegate": True
        }
    }
    response = client.post(
        '/v1/representees/100004/delegates/100005/mandates/150006/subdelegates',
        json=body
    )
    assert response.status_code == 422
    assert response.json == {
        'href': 'http://example-unprocessable-request-error-guidence.com',
        'title': 'Mandate to sub-delegate (id=150006) has deleted=TRUE\nCONTEXT:  PL/pgSQL function paasuke_add_mandate_subdelegate(text,text,text,text,text,text,text,text,date,date,text,text,boolean) line 27 at RAISE\n',
        'translation': {
            'en': 'Unprocessable request error',
            'et': 'Unprocessable request error (et)',
            'ru': 'Unprocessable request error (ru)'
        },
        'type': 'test-type-for-internal-server-error-found'
    }


def test_roles(client):
    response = client.get('v1/roles')
    assert response.status_code == 200
    assert response.json == [
        {
            'addableBy': [
                'BR_REPRIGHT:SOLEREP',
                'AGENCY_X:MANDATES_MANAGER'
            ],
            'addingMustBeSigned': False,
            'code': 'AGENCY_X:ENTER',
            'delegateMustEqualToRepresenteeOnAdd': False,
            'delegateType': ['NATURAL_PERSON'],
            'description': {
                'en': 'Omab õigust sisestada andmeid',
                'et': 'Has the right to enter data',
                'ru': 'Has the right to enter data (ru)'
            },
            'hidden': False,
            'representeeType': ['LEGAL_PERSON'],
            'subDelegable': 'NO',
            'subDelegatingMustBeSigned': False,
            'title': {
                'en': 'Andmesisestaja',
                'et': 'Data entry specialist',
                'ru': 'Andmesisestaja (ru)'
            },
            'validityPeriodFromNotInFuture': True,
            'validityPeriodThroughMustBeUndefined': True,
            'waivableBy': ['NAT_REPRIGHT:SOLEREP'],
            'waivingMustBeSigned': False,
            'withdrawableBy': [
                'BR_REPRIGHT:SOLEREP',
                'AGENCY_X:MANDATES_MANAGER'
            ],
            'withdrawalMustBeSigned': False
        },
        {
            'addableBy': [
                'BR_REPRIGHT:SOLEREP',
                'AGENCY_X:MANDATES_MANAGER'
            ],
            'addingMustBeSigned': False,
            'code': 'AGENCY_X:ENTER_AND_SUBMIT',
            'delegateMustEqualToRepresenteeOnAdd': False,
            'delegateType': ['NATURAL_PERSON'],
            'description': {
                'en': 'Omab õigust sisestada andmeid ja neid esitada',
                'et': 'Has the right to enter data and submit them',
                'ru': 'Has the right to enter data and submit them (ru)'
            },
            'hidden': False,
            'representeeType': ['LEGAL_PERSON'],
            'subDelegable': 'NO',
            'subDelegatingMustBeSigned': False,
            'title': {
                'en': 'Esitamisõigusega andmesisestaja',
                'et': 'Data entry and report submitting specialist',
                'ru': 'Data entry and report submitting specialist (ru)'
            },
            'validityPeriodFromNotInFuture': True,
            'validityPeriodThroughMustBeUndefined': True,
            'waivableBy': ['NAT_REPRIGHT:SOLEREP'],
            'waivingMustBeSigned': False,
            'withdrawableBy': [
                'BR_REPRIGHT:SOLEREP',
                'AGENCY_X:MANDATES_MANAGER'
            ],
            'withdrawalMustBeSigned': False
        },
        {
            'addableBy': ['BR_REPRIGHT:SOLEREP'],
            'addableOnlyIfRepresenteeHasRoleIn': ['BR_REPRIGHT:SOLEREP'],
            'addingMustBeSigned': False,
            'code': 'AGENCY_X:MANDATES_MANAGER',
            'delegateMustEqualToRepresenteeOnAdd': False,
            'delegateType': [
                'LEGAL_PERSON',
                'NATURAL_PERSON'
            ],
            'description': {
                'en': 'Omab õigust volitusi lisada ja muuta',
                'et': 'Has the right to edit and add mandates',
                'ru': 'Has the right to edit and add mandates (ru)'
            },
            'hidden': False,
            'representeeIdentifierIn': ['EE44444444'],
            'representeeType': [
                'LEGAL_PERSON',
                'NATURAL_PERSON'
            ],
            'subDelegable': 'YES',
            'subDelegableBy': ['BR_REPRIGHT:SOLEREP'],
            'subDelegateType': ['NATURAL_PERSON'],
            'subDelegatingMustBeSigned': False,
            'title': {
                'en': 'Volituste haldur',
                'et': 'Mandates manager',
                'ru': 'Mandates manager (ru)'
            },
            'validityPeriodFromNotInFuture': True,
            'validityPeriodThroughMustBeUndefined': True,
            'waivableBy': ['NAT_REPRIGHT:SOLEREP'],
            'waivingMustBeSigned': False,
            'withdrawableBy': ['BR_REPRIGHT:SOLEREP'],
            'withdrawalMustBeSigned': False
        }
    ]
