
# Adapter application (Python)

This application is an adapter for [Pääsuke](https://github.com/e-gov/PH) written in Python Flask.
This can be used by a party who keeps mandates on their side and offers a standard web service
for Pääsuke for it to query mandates.

The idea is that there is a Postgres database that keeps the data.
Into that Postgres database we create view and stored procedures that this app calls.

## Sequence diagram illustrating the application
![Sequence diagram](doc/sequence-diagram-pr.png)


## How this application differs from mocks

There is an application that mimics the different parties:
https://github.com/e-gov/PH/tree/main/ph-xroad-api-mock
The mock does not keep state. This application does.

## Prerequisite

Use Docker-compose to start up a Postgres database.
This database has a few tables to sore information about mandates.


## How this app was made

1. Open https://app.swaggerhub.com/apis/aasaru/x-road-services-consumed-by-paasuke/0.8.0#/
2. Export server stub -> python flask


## Configuration

## How to run API app in development environment

    `python3 -m venv venv`
    `source venv/bin/activate`
    `pip install -r requirements.txt`
    `export PYTHONPATH=$PWD`

Check configuration example in example.cfg.

    `cp config/example.cfg config/dev.cfg`

    `export APP_SETTINGS=../config/dev.cfg`

    `python3 api/app.py`

## How to run API app with docker-compose
    `docker-compose up -d`

## How to configure the list of roles

Configure the list of roles in tests/pg_data/02b_view_paasuke_roles_view.sql


## How to run tests

Tests are using the Postgres database running on a Docker container (so you need to have `docker-compose up postgres`)
Database contains fixture data .
    `python3 -m venv venv`
    `source venv/bin/activate`
    `pip install -r requirements.txt`
    `export PYTHONPATH=$PWD`
    `export APP_SETTINGS=../config/test.cfg`
    `pytest`

## How to run API app using WSGI and gunicorn

    `pip install gunicorn`

Point gunicorn to WSGI entrypoint `wsgi.py`

    `gunicorn --bind 127.0.0.1:5001 wsgi:application`


## Endpoints

When running locally then access API on http://localhost:8082


### `GET /v1/representees/<str:representee>/delegates/mandates`

Accepts representee identifier as parameter in path
Raises `400` error if identifier is not valid
Returns the list of `MandateTriplet`s with status code `200` if representee has valid mandates
Returns empty list if the representee has no valid mandates or the representee is unknown.
Selects data from Postgres view `paasuke_mandates_view`

Example:
```
curl --location 'http://localhost:8082/v1/representees/EE44444444/delegates/mandates' \
--header 'X-Road-UserId: test-header-xroad-userid' \
--header 'X-Road-Represented-Party: test-header-xroad-represented-party' \
--header 'X-Road-Id: test-header-xroad-id'
```


### `GET /v1/delegates/<str:delegate>/representees/mandates`

Accepts delegate identifier as parameter in path
Raises `400` error if identifier is not valid
Returns the list of `MandateTriplet`s with status code `200` if delegate has valid mandates
Returns an empty list if delegate has no valid mandates or the delegate is unknown.
Selects data from Postgres view `paasuke_mandates_view`

Example:
```
curl --location 'http://127.0.0.1:8082/v1/delegates/EE22202222222/representees/mandates' \
--header 'X-Road-UserId: Test User Id'
```

### `GET /roles`

Get a list of roles
Selects data from Postgres view `paasuke_roles_view`

Example:

`curl --location 'http://localhost:8082/v1/roles'`



### `POST /v1/representees/<str:representee>/delegates/<str:delegate>/mandates`

Accepts repreentee and delegate identifiers as path parameters
Raises `400` error if payload data is not valid or identifiers are not valid
Raises `422` error if Postgres function `paasuke_add_mandate` does not validate input data.
Return an empty list with status code `201` in case of success

Example of successful request:

```
curl --location 'http://127.0.0.1:8082/v1/representees/EE12345678/delegates/EE38302250123/mandates' \
--header 'Content-Type: application/json' \
--header 'X-Road-UserId: LT123456' \
--header 'X-Road-Represented-Party: LV1234566' \
--data '  {
  "authorizations": [
    {
      "hasRole": "BR_REPRIGHT:JUHL_SOLEREP",
      "userIdentifier": "EE49028099999"
    }
  ],
  "representee": {
    "identifier": "EE12345678",
    "legalName": "Väikefirma OÜ",
    "type": "LEGAL_PERSON"
  },
  "delegate": {
    "firstName": "Jüri",
    "identifier": "EE38302250123",
    "surname": "Juurikas",
    "type": "NATURAL_PERSON"
  },
  "document": {
    "singleDelegate": true,
    "uuid": "5b72e01c-fa7f-479c-b014-cc19efe5b732"
  },
  "mandate": {
    "canSubDelegate": true,
    "role": "AGENCY_X:MANDATES_MANAGER",
    "validityPeriod": {
      "from": "2028-01-01",
      "through": "2030-12-31"
    }
  }
}'
```


### `POST /v1/representees/<representeeId>/delegates/<delegateId>/mandates/<mandateId>/subdelegates`

Accepts `representeeId`, `delegateId`, `mandateId` as parameters in the path.
Raises `404` error if the mandate does not exist
Raises `422` error if Postgres function `paasuke_add_mandate_subdelegate` does not validate input data.
Returns empty list with status code `200` in success case

Example of successful request:

```
curl --location 'http://127.0.0.1:8082/v1/representees/100004/delegates/100005/mandates/150003/subdelegates' \
--header 'Content-Type: application/json' \
--header 'X-Road-UserId: EE23232323' \
--header 'X-Road-Represented-Party: EE2323224444' \
--data '{
  "authorizations": [
    {
      "hasRole": "BR_REPRIGHT:PROK_SOLEREP",
      "userIdentifier": "EE39912310123"
    }
  ],
  "document": {
    "singleDelegate": true,
    "uuid": "5b72e01c-fa7f-479c-b014-cc19efe5b732"
  },
  "subDelegate": {
    "firstName": "Jüri",
    "identifier": "EE38302250123",
    "surname": "Juurikas",
    "type": "NATURAL_PERSON"
  },
  "validityPeriod": {
    "from": "2028-01-01",
    "through": "2030-12-31"
  }
}'
```


### `PUT /v1/representees/<representeeId>/delegates/<delegateId>/mandates/<mandateId>`

Accepts `representeeId`, `delegateId`, `mandateId` as parameters in the path.
Raises `404` error if the mandate does not exist
Raises `422` error if Postgres function `paasuke_delete_mandate` does not validate input data.
Returns empty list with status code `200` if mandates has been marked deleted successfully

Example of successful request:
```
curl --location --request PUT 'http://127.0.0.1:8082/v1/representees/100001/delegates/100003/mandates/150002' \
--header 'Content-Type: application/json' \
--data '{
  "action": "DELETE",
  "authorizations": [
    {
      "userIdentifier": "EE39912310123",
      "hasRole": "BR_REPRIGHT:SOLEREP"
    }
  ],
  "document": {
    "uuid": "5b72e01c-fa7f-479c-b014-cc19efe5b732",
    "singleDelegate": true
  }
}'


```











