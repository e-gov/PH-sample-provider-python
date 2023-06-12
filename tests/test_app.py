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
            'representee': {
                'identifier': 'EE11111111',
                'legalName': 'EE Legal Person 1',
                'type': 'LEGAL_PERSON'
            },
            'delegate': {
                'firstName': 'EE First Name',
                'identifier': 'EE22202222222',
                'surname': 'EE Surname 2',
                'type': 'NATURAL_PERSON'
            },
            'mandates': [
                {
                    'role': 'AGENCY_X:ENTER',
                    'links': {
                        'delete': '/v1/representees/100001/delegates/100002/mandates/150001',
                        'origin': 'http://example.com/'
                    }
                }
            ]
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
            'representee': {
                'identifier': 'EE11111111',
                'legalName': 'EE Legal Person 1',
                'type': 'LEGAL_PERSON'
            },
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
                        'origin': 'http://example.com/'
                    },
                    'role': 'AGENCY_X:ENTER'
                }
            ]
        },
        {
            'representee': {
                'identifier': 'EE11111111',
                'legalName': 'EE Legal Person 1',
                'type': 'LEGAL_PERSON'
            },
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
                        'origin': 'http://example.com/'
                    },
                    'role': 'AGENCY_X:ENTER_AND_SUBMIT',
                    'validityPeriod': {
                        'from': '2021-01-01'
                    }
                }
            ]
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
            'representee': {
                'identifier': 'EE11111111',
                'legalName': 'EE Legal Person 1',
                'type': 'LEGAL_PERSON'
            },
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
                        'origin': 'http://example.com/'
                    },
                    'role': 'AGENCY_X:ENTER'
                }
            ]
        },
    ]


def test_representee_mandates_filter_by_sub_delegated_by(client):
    response = client.get(
        'v1/representees/EE44444444/delegates/mandates',
        query_string={'subDelegatedBy': 'EE55555555'}

    )
    assert response.status_code == 200
    assert response.json == [
        {
            'representee': {
                'identifier': 'EE44444444',
                'legalName': 'EE Legal Person 4',
                'type': 'LEGAL_PERSON'
            },
            'delegate': {
                'firstName': 'EE First Name',
                'identifier': 'EE60606666666',
                'surname': 'EE Surname 6',
                'type': 'NATURAL_PERSON'
            },
            'mandates': [
                {
                    'role': 'AGENCY_X:MANDATES_MANAGER',
                    'subDelegatorIdentifier': 'EE55555555',
                    'validityPeriod': {
                        'from': '2020-01-01',
                        'through': '2030-12-31'
                    },
                    'links': {
                        'delete': '/v1/representees/100004/delegates/150006/mandates/150004',
                        'origin': 'http://example.com/'
                    }
                }
            ]

         }
    ]


def test_roles(client):
    response = client.get('v1/roles')
    assert response.status_code == 200
    assert response.json == [
        {
            'addableBy': ['BR_REPRIGHT:SOLEREP', 'AGENCY_X:MANDATES_MANAGER'],
            'addingMustBeSigned': False,
            'assignableBy': ['BR_REPRIGHT:SOLEREP', 'AGENCY_X:MANDATES_MANAGER'],
            'canSubDelegate': False,
            'code': 'AGENCY_X:ENTER',
            'delegateCanEqualToRepresentee': False,
            'deletableBy': ['BR_REPRIGHT:SOLEREP', 'AGENCY_X:MANDATES_MANAGER'],
            'deletableByDelegate': True,
            'description': {
                'en': 'Omab õigust sisestada andmeid',
                'et': 'Has the right to enter data',
                'ru': 'Has the right to enter data (ru)'},
            'representeeType': ['LEGAL_PERSON'],
            'title': {
                'en': 'Andmesisestaja',
                'et': 'Data entry specialist',
                'ru': 'Andmesisestaja (ru)'
            },
            'validityPeriodFromNotInFuture': True,
            'validityPeriodThroughMustBeUndefined': True,
            'visible': True, 
            'waivableBy': ['NAT_REPRIGHT:SOLEREP'],
            'waivingMustBeSigned': False,
            'withdrawableBy': ['BR_REPRIGHT:SOLEREP', 'AGENCY_X:MANDATES_MANAGER'],
            'withdrawalMustBeSigned': False},
        {
            'addableBy': ['BR_REPRIGHT:SOLEREP', 'AGENCY_X:MANDATES_MANAGER'],
            'addingMustBeSigned': False,
            'assignableBy': ['BR_REPRIGHT:SOLEREP', 'AGENCY_X:MANDATES_MANAGER'],
            'canSubDelegate': False,
            'code': 'AGENCY_X:ENTER_AND_SUBMIT',
            'delegateCanEqualToRepresentee': False,
            'deletableBy': ['BR_REPRIGHT:SOLEREP', 'AGENCY_X:MANDATES_MANAGER'],
            'deletableByDelegate': True,
            'description': {
                'en': 'Omab õigust sisestada andmeid ja neid esitada',
                'et': 'Has the right to enter data and submit them',
                'ru': 'Has the right to enter data and submit them (ru)'},
            'representeeType': ['LEGAL_PERSON'],
            'title': {
                'en': 'Esitamisõigusega andmesisestaja',
                'et': 'Data entry and report submitting specialist',
                'ru': 'Data entry and report submitting specialist (ru)'
            },
            'validityPeriodFromNotInFuture': True,
            'validityPeriodThroughMustBeUndefined': True,
            'visible': True,
            'waivableBy': ['NAT_REPRIGHT:SOLEREP'],
            'waivingMustBeSigned': False,
            'withdrawableBy': ['BR_REPRIGHT:SOLEREP', 'AGENCY_X:MANDATES_MANAGER'],
            'withdrawalMustBeSigned': False
        },
        {
            'addableBy': ['BR_REPRIGHT:SOLEREP'],
            'addingMustBeSigned': False,
            'assignableBy': ['BR_REPRIGHT:SOLEREP'],
            'canSubDelegate': False,
            'code': 'AGENCY_X:MANDATES_MANAGER',
            'delegateCanEqualToRepresentee': False,
            'deletableBy': ['BR_REPRIGHT:SOLEREP'],
            'deletableByDelegate': True,
            'description': {
                'en': 'Omab õigust volitusi lisada ja muuta',
                'et': 'Has the right to edit and add mandates',
                'ru': 'Has the right to edit and add mandates (ru)'},
            'representeeType': ['LEGAL_PERSON', 'NATURAL_PERSON'],
            'title': {
                'en': 'Volituste haldur',
                'et': 'Mandates manager',
                'ru': 'Mandates manager (ru)'
            },
            'validityPeriodFromNotInFuture': True,
            'validityPeriodThroughMustBeUndefined': True,
            'visible': True,
            'waivableBy': ['NAT_REPRIGHT:SOLEREP'],
            'waivingMustBeSigned': False,
            'withdrawableBy': ['BR_REPRIGHT:SOLEREP'],
            'withdrawalMustBeSigned': False},
    ]
