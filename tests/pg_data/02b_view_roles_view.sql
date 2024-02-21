CREATE OR REPLACE VIEW paasuke_roles_view AS
SELECT
    'AGENCY_X:ENTER' AS code,
    'Andmesisestaja' AS title_en,
    'Data entry specialist' AS title_et,
    'Andmesisestaja (ru)' AS title_ru,

    'Omab õigust sisestada andmeid' AS description_en,
    'Has the right to enter data' AS description_et,
    'Has the right to enter data (ru)' AS description_ru,

    ARRAY [ 'BR_REPRIGHT:SOLEREP', 'AGENCY_X:MANDATES_MANAGER' ]::TEXT[] AS addable_by,
    FALSE AS adding_must_be_signed,
    'NO' AS sub_delegable,
    ARRAY []::TEXT[] AS sub_delegate_type,
    ARRAY []::TEXT[] AS sub_delegable_by,
    FALSE AS sub_delegating_must_be_signed,
    ARRAY ['LEGAL_PERSON']::TEXT[] AS representee_type,
    ARRAY ['NATURAL_PERSON']::TEXT[] AS delegate_type,
    ARRAY ['NAT_REPRIGHT:SOLEREP']::TEXT[] AS waivable_by,
    FALSE AS waiving_must_be_signed,
    ARRAY ['BR_REPRIGHT:SOLEREP', 'AGENCY_X:MANDATES_MANAGER']::TEXT[] AS withdrawable_by,
    FALSE AS withdrawal_must_be_signed,

    -- values that are used in rare cases
    ARRAY []::TEXT[] AS addable_only_if_representee_has_role_in,
    FALSE AS delegate_must_equal_to_representee,
    TRUE AS validity_period_from_not_in_future,
    TRUE AS validity_period_through_must_be_undefined,
    ARRAY []::TEXT[] AS representee_identifier_in,
    FALSE AS hidden

UNION

SELECT
    'AGENCY_X:ENTER_AND_SUBMIT' AS code,
    'Esitamisõigusega andmesisestaja' AS title_en,
    'Data entry and report submitting specialist' AS title_et,
    'Data entry and report submitting specialist (ru)' AS title_ru,

    'Omab õigust sisestada andmeid ja neid esitada' AS description_en,
    'Has the right to enter data and submit them' AS description_et,
    'Has the right to enter data and submit them (ru)' AS description_ru,

    ARRAY [ 'BR_REPRIGHT:SOLEREP', 'AGENCY_X:MANDATES_MANAGER' ]::TEXT[] AS addable_by,
    FALSE AS adding_must_be_signed,
    'NO' AS sub_delegable,
    ARRAY []::TEXT[] AS sub_delegate_type,
    ARRAY []::TEXT[] AS sub_delegable_by,
    FALSE AS sub_delegating_must_be_signed,
    ARRAY ['LEGAL_PERSON']::TEXT[] AS representee_type,
    ARRAY ['NATURAL_PERSON']::TEXT[] AS delegate_type,
    ARRAY ['NAT_REPRIGHT:SOLEREP']::TEXT[] AS waivable_by,
    FALSE AS waiving_must_be_signed,
    ARRAY ['BR_REPRIGHT:SOLEREP', 'AGENCY_X:MANDATES_MANAGER']::TEXT[] AS withdrawable_by,
    FALSE AS withdrawal_must_be_signed,

    -- values that are used in rare cases
    ARRAY []::TEXT[] AS addable_only_if_representee_has_role_in,
    FALSE AS delegate_must_equal_to_representee,
    TRUE AS validity_period_from_not_in_future,
    TRUE AS validity_period_through_must_be_undefined,
    ARRAY []::TEXT[] AS representee_identifier_in,
    FALSE AS hidden

UNION

SELECT
    'AGENCY_X:MANDATES_MANAGER' AS code,
    'Volituste haldur' AS title_en,
    'Mandates manager' AS title_et,
    'Mandates manager (ru)' AS title_ru,

    'Omab õigust volitusi lisada ja muuta' AS description_en,
    'Has the right to edit and add mandates' AS description_et,
    'Has the right to edit and add mandates (ru)' AS description_ru,

    ARRAY ['BR_REPRIGHT:SOLEREP']::TEXT[] AS addable_by,
    FALSE AS adding_must_be_signed,
    'YES' AS sub_delegable,
    ARRAY ['NATURAL_PERSON']::TEXT[] AS sub_delegate_type,
    ARRAY ['BR_REPRIGHT:SOLEREP']::TEXT[] AS sub_delegable_by,
    FALSE AS sub_delegating_must_be_signed,
    ARRAY ['LEGAL_PERSON', 'NATURAL_PERSON']::TEXT[] AS representee_type,
    ARRAY ['LEGAL_PERSON','NATURAL_PERSON']::TEXT[] AS delegate_type,
    ARRAY ['NAT_REPRIGHT:SOLEREP']::TEXT[] AS waivable_by,
    FALSE AS waiving_must_be_signed,
    ARRAY ['BR_REPRIGHT:SOLEREP']::TEXT[] AS withdrawable_by,
    FALSE AS withdrawal_must_be_signed,

    -- values that are used in rare cases
    ARRAY ['BR_REPRIGHT:SOLEREP']::TEXT[] AS addable_only_if_representee_has_role_in,
    FALSE AS delegate_must_equal_to_representee,
    TRUE AS validity_period_from_not_in_future,
    TRUE AS validity_period_through_must_be_undefined,
    ARRAY ['EE44444444']::TEXT[] AS representee_identifier_in,
    FALSE AS hidden
;
