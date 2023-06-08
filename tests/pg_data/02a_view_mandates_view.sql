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
