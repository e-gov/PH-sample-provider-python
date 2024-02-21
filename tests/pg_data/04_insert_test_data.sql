ALTER SEQUENCE person_id_seq RESTART WITH 100101;
ALTER SEQUENCE mandate_id_seq RESTART WITH 150101;

insert into person(id, type, personal_company_code, personal_company_code_country,  legal_name) values(100001, 'LEGAL_PERSON', '11111111', 'EE', 'EE Legal Person 1');
insert into person(id, type, personal_company_code, personal_company_code_country, first_name, surname) values(100002, 'NATURAL_PERSON', '22202222222', 'EE', 'EE First Name', 'EE Surname 2');
insert into person(id, type, personal_company_code, personal_company_code_country, first_name, surname) values(100003, 'NATURAL_PERSON', '33303333333', 'LT', 'LT First', 'LT Surname 2');

insert into person(id, type, personal_company_code, personal_company_code_country, legal_name) values(100004, 'LEGAL_PERSON', '44444444', 'EE', 'EE Legal Person 4');
insert into person(id, type, personal_company_code, personal_company_code_country, legal_name) values(100005, 'LEGAL_PERSON', '55555555', 'EE', 'EE Legal Person 5');
insert into person(id, type, personal_company_code, personal_company_code_country, first_name, surname) values(100006, 'NATURAL_PERSON', '60606666666', 'EE', 'EE First Name', 'EE Surname 6');


INSERT INTO mandate(id, representee_id, delegate_id, role, validity_period_from, validity_period_through, can_sub_delegate, created_by) VALUES(150001, 100001, 100002, 'AGENCY_X:ENTER', NULL, NULL, FALSE, 100001);
INSERT INTO mandate(id, representee_id, delegate_id, role, validity_period_from, validity_period_through, can_sub_delegate, created_by) VALUES(150002, 100001, 100003, 'AGENCY_X:ENTER_AND_SUBMIT', '2021-01-01', NULL, FALSE, 100001);

INSERT INTO mandate(id, representee_id, delegate_id, role, validity_period_from, validity_period_through, can_sub_delegate, created_by) VALUES(150003, 100004, 100005, 'AGENCY_X:MANDATES_MANAGER', NULL, '2044-12-31', TRUE, 100004);
INSERT INTO mandate(id, representee_id, delegate_id, role, validity_period_from, validity_period_through, can_sub_delegate, created_by, original_mandate_id) VALUES(150004, 100004, 100006, 'AGENCY_X:MANDATES_MANAGER', '2020-01-01', '2030-12-31', FALSE, 100005, 150003);
INSERT INTO mandate(id, representee_id, delegate_id, role, validity_period_from, validity_period_through, can_sub_delegate, created_by) VALUES(150005, 100004, 100005, 'AGENCY_X:MANDATES_MANAGER', NULL, '2050-12-31', TRUE, 100004);
INSERT INTO mandate(id, representee_id, delegate_id, role, validity_period_from, validity_period_through, can_sub_delegate, created_by, original_mandate_id, deleted) VALUES(150006, 100004, 100005, 'AGENCY_X:MANDATES_MANAGER', NULL, '2050-12-31', TRUE, 100004, NULL, TRUE);
