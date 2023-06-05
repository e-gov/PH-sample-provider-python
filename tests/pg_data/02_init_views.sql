CREATE OR REPLACE VIEW representee_mandates_view AS
SELECT
    mandate.id AS mandate_id,
    mandate.delegate_id,
    delegate.personal_company_code_country || delegate.personal_company_code AS delegate_identifier,
    delegate.type AS delegate_type,
    delegate.first_name AS delegate_first_name,
    delegate.surname AS delegate_surname,
    delegate.legal_name AS delegate_legal_name,
    mandate.representee_id,
    representee.personal_company_code_country || representee.personal_company_code AS representee_identifier,
    representee.type AS representee_type,
    representee.first_name AS representee_first_name,
    representee.surname AS representee_surname,
    representee.legal_name AS representee_legal_name,
    mandate.role,
    mandate.validity_period_from::DATE,
    mandate.validity_period_through::DATE,
    mandate.can_sub_delegate,
    mandate.created_by,
    mandate.created_by_represented_person,
    mandate.original_mandate_id,
    mandate.document_uuid,
    mandate.can_display_document_to_delegate,
    CONCAT('/v1/representees/', mandate.representee_id, '/delegates/', mandate.delegate_id, '/mandates/', mandate.id) AS link_delete,
    CASE
        WHEN mandate.can_sub_delegate IS TRUE THEN CONCAT('/v1/representees/', mandate.representee_id, '/delegates/', mandate.delegate_id, '/mandates/', mandate.id, '/subdelegates')
        ELSE mandate.link_add_sub_delegate
    END AS link_add_sub_delegate
FROM mandate
JOIN person AS delegate ON delegate.id = mandate.delegate_id
JOIN person AS representee ON representee.id = mandate.representee_id
WHERE mandate.deleted is NOT TRUE;


CREATE VIEW roles_view AS
--CREATE VIEW roles_view AS
SELECT
    'ANNUAL_REPORTS:ENTER' as code,
    'Andmesisestaja' as title_en,
    'Data entry specialist' as title_et,
    'Andmesisestaja (rus)' as title_ru,
    '2023-05-31T12:00:00'::timestamp as modified,

    'Omab õigust sisestada majandusaasta aruande andmeid' as description_en,
    'Has the right to enter annual report data' as description_et,
    'Omab õigust sisestada majandusaasta aruande andmeid (rus)' as description_ru,

    ARRAY [ 'BR_REPRIGHT:SOLEREP' ]::text[] as addable_by,

    false as adding_must_be_signed,
    false as can_sub_delegate,
    ARRAY ['LEGAL_PERSON']::text[] as representee_type,
    ARRAY ['NATURAL_PERSON']::text[] as delegateType,
    ARRAY ['NAT_REPRIGHT:SOLEREP']::text[] as waivable_by,
    false as waiving_must_be_signed,
    ARRAY ['BR_REPRIGHT:SOLEREP']::text[] as withdrawable_by,
    false as withdrawal_must_be_signed,

    -- values that are used in rare cases
    null as addable_only_if_representee_has_role_in,
    false as delegate_can_equal_to_representee,
    true as validity_period_from_not_in_future,
    true as validity_period_through_must_be_undefined,

    -- deprecated since 0.9.0
    ARRAY ['BR_REPRIGHT:SOLEREP']::text[] as assignable_by,
    ARRAY ['BR_REPRIGHT:SOLEREP']::text[]::text[]::text[] as deletable_by,
    null as assignable_only_if_representee_has_role_in,
    True as deletable_by_delegate,
    True as visible

UNION

SELECT
    'ANNUAL_REPORTS:ENTER_AND_SUBMIT' as code,
    'Esitamisõigusega andmesisestaja' as title_en,
    'Data entry and report submitting specialist' as title_et,
    'Esitamisõigusega andmesisestaja (rus)' as title_ru,
    '2023-05-31T12:00:00'::timestamp as modified,

    'Omab õigust sisestada majandusaasta aruande andmeid ja esitada aruanne registrile' as description_en,
    'Has the right to enter annual report data and submit annual reports to the business registry' as description_et,
    'Omab õigust sisestada majandusaasta aruande andmeid ja esitada aruanne registrile (rus)' as description_ru,

    ARRAY [ 'BR_REPRIGHT:SOLEREP' ]::text[] as addable_by,
    false as adding_must_be_signed,
    false as can_sub_delegate,
    ARRAY ['LEGAL_PERSON']::text[] as representee_type,
    ARRAY ['NATURAL_PERSON']::text[] as delegate_type,
    ARRAY ['NAT_REPRIGHT:SOLEREP']::text[] as waivable_by,
    false as waiving_must_be_signed,
    ARRAY ['BR_REPRIGHT:SOLEREP']::text[] as withdrawable_by,
    false as withdrawal_must_be_signed,

    -- values that are used in rare cases
    null as addable_only_if_representee_has_role_in,
    false as delegate_can_equal_to_representee,
    true as validity_period_from_not_in_future,
    true as validity_period_through_must_be_undefined,

    -- deprecated since 0.9.0
    ARRAY ['BR_REPRIGHT:SOLEREP']::text[] as assignable_by,
    ARRAY []::text[] as deletable_by,
    null as assignable_only_if_representee_has_role_in,
    True as deletable_by_delegate,
    True as visible
