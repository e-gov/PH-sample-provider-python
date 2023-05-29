ALTER SEQUENCE person_id_seq RESTART WITH 100001;
ALTER SEQUENCE mandate_id_seq RESTART WITH 150000;

insert into person(type, personal_company_code, personal_company_code_country, first_name, surname, legal_name) values('NATURAL_PERSON', '1234568', 'LT', 'LT Person Name 1', 'LT Person Surname 1', 'LT Legal Person 1');
insert into person(type, personal_company_code, personal_company_code_country, first_name, surname, legal_name) values('LEGAL_PERSON', '1111111', 'EE', 'EE Person Name 1', 'EE Person Surname 1', 'EE Legal Person 1');
insert into person(type, personal_company_code, personal_company_code_country, first_name, surname, legal_name) values('UNKNOWN', '2222222', 'EE', 'EE Person Name 2', 'EE Person Surname 2', 'EE Legal Person 2');
insert into person(type, personal_company_code, personal_company_code_country, first_name, surname, legal_name) values('LEGAL_PERSON', '33333333', 'EE', 'EE Person Name 3', 'EE Person Surname 3', 'EE Legal Person 3');
insert into person(type, personal_company_code, personal_company_code_country, first_name, surname, legal_name) values('OTHER', '98765432', 'LV', 'LV Person Name 1', 'EE Person Surname 1', 'EE Legal Person 1');

INSERT INTO mandate(representee_id, delegate_id, role, validity_period_from, validity_period_through, can_sub_delegate, created_by, created_by_represented_person) VALUES(100004, 100002, 'TEST:ROLE1', NULL, NULL, TRUE, 'test', 'test');
INSERT INTO mandate(representee_id, delegate_id, role, validity_period_from, validity_period_through, can_sub_delegate, created_by, created_by_represented_person) VALUES(100004, 100002, 'TEST:ROLE1', '2021-01-01', NULL, FALSE, 'test', 'test');
INSERT INTO mandate(representee_id, delegate_id, role, validity_period_from, validity_period_through, can_sub_delegate, created_by, created_by_represented_person) VALUES(100004, 100002, 'TEST:ROLE2', NULL, '2018-12-31', FALSE, 'test', 'test');
INSERT INTO mandate(representee_id, delegate_id, role, validity_period_from, validity_period_through, can_sub_delegate, created_by, created_by_represented_person) VALUES(100004, 100001, 'TEST2:ROLE2:ROLE6', '2020-01-01', '2030-12-31', TRUE, 'test', 'test');
INSERT INTO mandate(representee_id, delegate_id, role, validity_period_from, validity_period_through, can_sub_delegate, created_by, created_by_represented_person) VALUES(100004, 100001, 'TEST3:ROLE12:ROLE100', NULL, '2050-12-31', TRUE, 'test', 'test');

INSERT INTO mandate(representee_id, delegate_id, role, validity_period_from, validity_period_through, can_sub_delegate, created_by, created_by_represented_person) VALUES(100005, 100002, 'TEST6:ROLE1:ROLE2', NULL, '2050-12-31', TRUE, 'test', 'test');