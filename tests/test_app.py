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
    response = client.get('/delegates/1EE1234567/representees/mandates')
    assert response.status_code == 400
    error_config = config['SETTINGS']['errors']['legal_person_format_validation_failed']

    assert response.json == {
        'href': error_config['reference'],
        'title': 'Legal person validation failed',
        'translation': error_config['translation'],
        'type': error_config['type']
    }


def test_delegate_not_found_empty_list(client, config):
    response = client.get('/delegates/EE3333333/representees/mandates')
    assert response.status_code == 200
    assert response.json == []


def test_delegate_mandates(client):
    response = client.get('/delegates/EE1111111/representees/mandates')
    assert response.status_code == 200
    assert response.json == [
        {
            'delegate': {
                'firstName': 'EE Person Name 1',
                'identifier': 'EE1111111',
                'surname': 'EE Person Surname 1',
                'type': 'LEGAL_PERSON'
            },
            'mandates': [
                {
                    'links': {
                        'delete': '/v1/representees/100004/delegates/100002/mandates/150000',
                        'origin': 'http://example.com/',
                        'addSubDelegate': '/v1/representees/100004/delegates/100002/mandates/150000/subdelegates'
                    },
                    'role': 'TEST:ROLE1'
                },
                {
                    'links': {
                        'delete': '/v1/representees/100004/delegates/100002/mandates/150001',
                        'origin': 'http://example.com/'
                    },
                    'role': 'TEST:ROLE1',
                    'validityPeriod': {
                        'from': '2021-01-01'
                    }
                }
            ],
            'representee': {
                'identifier': 'EE33333333',
                'legalName': 'EE Legal Person 3',
                'type': 'LEGAL_PERSON'
            }
        },
        {
            'delegate': {
                'firstName': 'EE Person Name 1',
                'identifier': 'EE1111111',
                'surname': 'EE Person Surname 1',
                'type': 'LEGAL_PERSON'
            },
            'mandates': [
                {
                    'links': {
                        'delete': '/v1/representees/100005/delegates/100002/mandates/150005',
                        'origin': 'http://example.com/',
                        'addSubDelegate': '/v1/representees/100005/delegates/100002/mandates/150005/subdelegates'
                    },
                    'role': 'TEST6:ROLE1:ROLE2',
                    'validityPeriod': {
                        'through': '2050-12-31'
                    }
                }
            ],
            'representee': {
                'identifier': 'LV98765432',
                'legalName': 'EE Legal Person 1',
                'type': 'OTHER'
            }
        }
    ]


def test_representee_format_validation_failed(client, config):
    response = client.get('representees/1EE33333333/delegates/mandates')
    assert response.status_code == 400
    error_config = config['SETTINGS']['errors']['legal_person_format_validation_failed']

    assert response.json == {
        'href': error_config['reference'],
        'title': 'Legal person validation failed',
        'translation': error_config['translation'],
        'type': error_config['type']
    }


def test_representee_not_found_empty_list(client, config):
    response = client.get('/representees/EE4q486846/delegates/mandates')
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
        'representees/EE33333333/delegates/mandates',
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
    response = client.get('representees/EE33333333/delegates/mandates')
    assert response.status_code == 200
    assert response.json == [
        {
            'delegate':
                {
                    'identifier': 'EE1111111',
                    'legalName': 'EE Legal Person 1',
                    'type': 'LEGAL_PERSON'
                },
            'mandates': [
                {
                    'links':
                        {
                            'addSubDelegate': '/v1/representees/100004/delegates/100002/mandates/150000/subdelegates',
                            'delete': '/v1/representees/100004/delegates/100002/mandates/150000',
                            'origin': 'http://example.com/'
                        },
                    'role': 'TEST:ROLE1'
                },
                {
                    'links':
                        {
                            'delete': '/v1/representees/100004/delegates/100002/mandates/150001',
                            'origin': 'http://example.com/'
                        },
                    'role': 'TEST:ROLE1',
                    'validityPeriod':
                        {
                            'from': '2021-01-01'
                        }
                }
            ],
            'representee':
                {
                    'identifier': 'EE33333333',
                    'legalName': 'EE Legal Person 3',
                    'type': 'LEGAL_PERSON'
                }
        },
        {
            'delegate': {
                'firstName': 'LT Person Name 1',
                'identifier': 'LT1234568',
                'surname': 'LT Person Surname 1',
                'type': 'NATURAL_PERSON'
            },
            'mandates': [
                {
                    'links':
                        {
                            'addSubDelegate': '/v1/representees/100004/delegates/100001/mandates/150003/subdelegates',
                            'delete': '/v1/representees/100004/delegates/100001/mandates/150003',
                            'origin': 'http://example.com/'
                        },
                    'role': 'TEST2:ROLE2:ROLE6',
                    'validityPeriod':
                        {
                            'from': '2020-01-01',
                            'through': '2030-12-31'
                        }
                },
                {
                    'links':
                        {
                            'addSubDelegate': '/v1/representees/100004/delegates/100001/mandates/150004/subdelegates',
                            'delete': '/v1/representees/100004/delegates/100001/mandates/150004',
                            'origin': 'http://example.com/'
                        },
                    'role': 'TEST3:ROLE12:ROLE100',
                    'validityPeriod':
                        {
                            'through': '2050-12-31'
                        }
                }
            ],
            'representee':
                {
                    'identifier': 'EE33333333',
                    'legalName': 'EE Legal Person 3',
                    'type': 'LEGAL_PERSON'
                }
        }
    ]


def test_representee_mandates_filter_by_delegate(client):
    response = client.get(
        'representees/EE33333333/delegates/mandates',
        query_string={'delegate': 'LT1234568'}

    )
    assert response.status_code == 200
    assert response.json == [
        {
            'delegate': {
                'firstName': 'LT Person Name 1',
                'identifier': 'LT1234568',
                'surname': 'LT Person Surname 1',
                'type': 'NATURAL_PERSON'
            },
            'mandates': [
                {
                    'links': {
                        'delete': '/v1/representees/100004/delegates/100001/mandates/150003',
                        'origin': 'http://example.com/',
                        'addSubDelegate': '/v1/representees/100004/delegates/100001/mandates/150003/subdelegates'
                    },
                    'role': 'TEST2:ROLE2:ROLE6',
                    'validityPeriod': {
                        'from': '2020-01-01',
                        'through': '2030-12-31'
                    }
                },
                {
                    'links': {
                        'delete': '/v1/representees/100004/delegates/100001/mandates/150004',
                        'origin': 'http://example.com/',
                        'addSubDelegate': '/v1/representees/100004/delegates/100001/mandates/150004/subdelegates'
                    },
                    'role': 'TEST3:ROLE12:ROLE100',
                    'validityPeriod': {
                        'through': '2050-12-31'
                    }
                }
            ],
            'representee': {
                'identifier': 'EE33333333',
                'legalName': 'EE Legal Person 3',
                'type': 'LEGAL_PERSON'
            }
        },
    ]


def test_roles(client):
    response = client.get('roles')
    assert response.status_code == 200
    assert response.json == [
        {
            'addableBy': ['BR_REPRIGHT:SOLEREP'],
            'addingMustBeSigned': False,
            'assignableBy': ['BR_REPRIGHT:SOLEREP'],
            'canSubDelegate': False,
            'code': 'ANNUAL_REPORTS:ENTER',
            'delegateCanEqualToRepresentee': False,
            'deletableBy': ['BR_REPRIGHT:SOLEREP'],
            'deletableByDelegate': True,
            'description': {
                'en': 'Omab õigust sisestada majandusaasta aruande andmeid',
                'et': 'Has the right to enter annual report data',
                'ru': 'Omab õigust sisestada majandusaasta aruande andmeid (rus)'
            },
            'modified': '2023-05-31T12:00:00',
            'representeeType': ['LEGAL_PERSON'],
            'title': {
                'en': 'Andmesisestaja',
                'et': 'Data entry specialist',
                'ru': 'Andmesisestaja (rus)'
            },
            'validityPeriodFromNotInFuture': True,
            'validityPeriodThroughMustBeUndefined': True,
            'visible': True, 'waivableBy': ['NAT_REPRIGHT:SOLEREP'],
            'waivingMustBeSigned': False,
            'withdrawableBy': ['BR_REPRIGHT:SOLEREP'],
            'withdrawalMustBeSigned': False
        },
        {
            'addableBy': ['BR_REPRIGHT:SOLEREP'],
            'addingMustBeSigned': False,
            'assignableBy': ['BR_REPRIGHT:SOLEREP'],
            'canSubDelegate': False,
            'code': 'ANNUAL_REPORTS:ENTER_AND_SUBMIT',
            'delegateCanEqualToRepresentee': False,
            'deletableByDelegate': True,
            'description': {
                'en': 'Omab õigust sisestada majandusaasta aruande andmeid ja esitada aruanne registrile',
                'et': 'Has the right to enter annual report data and submit annual reports to the business registry',
                'ru': 'Omab õigust sisestada majandusaasta aruande andmeid ja esitada aruanne registrile (rus)'
            },
            'modified': '2023-05-31T12:00:00',
            'representeeType': ['LEGAL_PERSON'],
            'title': {
                'en': 'Esitamisõigusega andmesisestaja',
                'et': 'Data entry and report submitting specialist',
                'ru': 'Esitamisõigusega andmesisestaja (rus)'
            },
            'validityPeriodFromNotInFuture': True,
            'validityPeriodThroughMustBeUndefined': True,
            'visible': True,
            'waivableBy': ['NAT_REPRIGHT:SOLEREP'],
            'waivingMustBeSigned': False,
            'withdrawableBy': ['BR_REPRIGHT:SOLEREP'],
            'withdrawalMustBeSigned': False
        }
    ]
