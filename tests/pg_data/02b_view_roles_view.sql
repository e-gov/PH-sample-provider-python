CREATE OR REPLACE VIEW paasuke_roles_view AS
SELECT
    'AGENCY_X:ENTER' as code,
    'Andmesisestaja' as title_en,
    'Data entry specialist' as title_et,
    'Andmesisestaja (ru)' as title_ru,

    'Omab õigust sisestada andmeid' as description_en,
    'Has the right to enter data' as description_et,
    'Has the right to enter data (ru)' as description_ru,

    ARRAY [ 'BR_REPRIGHT:SOLEREP', 'AGENCY_X:MANDATES_MANAGER' ]::text[] as addable_by,

    false as adding_must_be_signed,
    false as can_sub_delegate,
    ARRAY ['LEGAL_PERSON']::text[] as representee_type,
    ARRAY ['NATURAL_PERSON']::text[] as delegateType,
    ARRAY ['NAT_REPRIGHT:SOLEREP']::text[] as waivable_by,
    false as waiving_must_be_signed,
    ARRAY ['BR_REPRIGHT:SOLEREP', 'AGENCY_X:MANDATES_MANAGER']::text[] as withdrawable_by,
    false as withdrawal_must_be_signed,

    -- values that are used in rare cases
    null as addable_only_if_representee_has_role_in,
    false as delegate_can_equal_to_representee,
    true as validity_period_from_not_in_future,
    true as validity_period_through_must_be_undefined,

    -- deprecated since 0.9.0
    ARRAY ['BR_REPRIGHT:SOLEREP', 'AGENCY_X:MANDATES_MANAGER']::text[] as assignable_by,
    ARRAY ['BR_REPRIGHT:SOLEREP', 'AGENCY_X:MANDATES_MANAGER']::text[] as deletable_by,
    null as assignable_only_if_representee_has_role_in,
    True as deletable_by_delegate,
    True as visible

UNION

SELECT
    'AGENCY_X:ENTER_AND_SUBMIT' as code,
    'Esitamisõigusega andmesisestaja' as title_en,
    'Data entry and report submitting specialist' as title_et,
    'Data entry and report submitting specialist (ru)' as title_ru,

    'Omab õigust sisestada andmeid ja neid esitada' as description_en,
    'Has the right to enter data and submit them' as description_et,
    'Has the right to enter data and submit them (ru)' as description_ru,

    ARRAY [ 'BR_REPRIGHT:SOLEREP', 'AGENCY_X:MANDATES_MANAGER' ]::text[] as addable_by,
    false as adding_must_be_signed,
    false as can_sub_delegate,
    ARRAY ['LEGAL_PERSON']::text[] as representee_type, -- this is list!
    ARRAY ['NATURAL_PERSON']::text[] as delegateType,
    ARRAY ['NAT_REPRIGHT:SOLEREP']::text[] as waivable_by,
    false as waiving_must_be_signed,
    ARRAY ['BR_REPRIGHT:SOLEREP', 'AGENCY_X:MANDATES_MANAGER']::text[] as withdrawable_by,
    false as withdrawal_must_be_signed,

    -- values that are used in rare cases
    null as addable_only_if_representee_has_role_in,
    false as delegate_can_equal_to_representee,
    true as validity_period_from_not_in_future,
    true as validity_period_through_must_be_undefined,

    -- deprecated since 0.9.0
    ARRAY ['BR_REPRIGHT:SOLEREP', 'AGENCY_X:MANDATES_MANAGER']::text[] as assignable_by,
    ARRAY ['BR_REPRIGHT:SOLEREP', 'AGENCY_X:MANDATES_MANAGER']::text[] as deletable_by,
    null as assignable_only_if_representee_has_role_in,
    True as deletable_by_delegate,
    True as visible


UNION

SELECT
    'AGENCY_X:MANDATES_MANAGER' as code,
    'Volituste haldur' as title_en,
    'Mandates manager' as title_et,
    'Mandates manager (ru)' as title_ru,

    'Omab õigust volitusi lisada ja muuta' as description_en,
    'Has the right to edit and add mandates' as description_et,
    'Has the right to edit and add mandates (ru)' as description_ru,

    ARRAY [ 'BR_REPRIGHT:SOLEREP']::text[] as addable_by,
    false as adding_must_be_signed,
    false as can_sub_delegate,
    ARRAY ['LEGAL_PERSON', 'NATURAL_PERSON']::text[] as representee_type,
    ARRAY ['LEGAL_PERSON','NATURAL_PERSON']::text[] as delegateType,
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
    ARRAY ['BR_REPRIGHT:SOLEREP']::text[] as deletable_by,
    null as assignable_only_if_representee_has_role_in,
    True as deletable_by_delegate,
    True as visible



;
