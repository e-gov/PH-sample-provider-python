CREATE OR REPLACE FUNCTION function_create_mandate(
    p_delegate_first_name TEXT,
    p_delegate_identifier TEXT,
    p_delegate_surname TEXT,
    p_delegate_type TEXT,
    p_representee_identifier TEXT,
    p_legal_name TEXT,
    p_representee_type TEXT,
    p_role TEXT,
    p_validity_period_from DATE,
    p_validity_period_through DATE,
    p_can_sub_delegate BOOLEAN,
    p_created_by TEXT,
    p_created_by_represented_person TEXT,
    p_original_mandate_id INTEGER,
    p_document_uuid TEXT,
    p_can_display_document_to_delegate BOOLEAN
) RETURNS VOID AS $$
DECLARE
    delegate_id INTEGER;
    representee_id INTEGER;
    dpcc TEXT := SUBSTRING(p_delegate_identifier FROM 3);
    dpccc TEXT := SUBSTRING(p_delegate_identifier FROM 1 FOR 2);
    rpcc TEXT := SUBSTRING(p_representee_identifier FROM 3);
    rpccc TEXT := SUBSTRING(p_representee_identifier FROM 1 FOR 2);
BEGIN
    -- Insert or update delegate person record
    INSERT INTO person (
        type, personal_company_code, personal_company_code_country, first_name, surname
    ) VALUES (
        p_delegate_type, dpcc, dpccc, p_delegate_first_name, p_delegate_surname
    )
    ON CONFLICT (personal_company_code, personal_company_code_country)
    DO UPDATE SET
        first_name = EXCLUDED.first_name,
        surname = EXCLUDED.surname
    RETURNING id INTO delegate_id;

    -- Insert or update representee person record
    INSERT INTO person (
        type, personal_company_code, personal_company_code_country, legal_name
    ) VALUES (
        p_representee_type, rpcc, rpccc, p_legal_name
    )
    ON CONFLICT (personal_company_code, personal_company_code_country)
    DO UPDATE SET
        legal_name = EXCLUDED.legal_name
    RETURNING id INTO representee_id;

    -- Insert mandate record
    INSERT INTO mandate (
        delegate_id, representee_id, role, validity_period_from, validity_period_through,
        can_sub_delegate, created_by, created_by_represented_person,
        original_mandate_id, document_uuid, can_display_document_to_delegate
    ) VALUES (
        delegate_id, representee_id, p_role, p_validity_period_from::DATE, p_validity_period_through::DATE,
        p_can_sub_delegate, p_created_by, p_created_by_represented_person,
        p_original_mandate_id, p_document_uuid, p_can_display_document_to_delegate
    );
END;
$$ LANGUAGE PLPGSQL;

CREATE OR REPLACE FUNCTION function_delete_mandate(
    p_representee_identifier TEXT,
    p_delegate_id TEXT, -- change to text type
    p_mandate_id TEXT -- change to text type
) RETURNS BOOLEAN AS $$
DECLARE
    v_representee_id INTEGER;
    rpcc TEXT := SUBSTRING(p_representee_identifier FROM 3);
    rpccc TEXT := SUBSTRING(p_representee_identifier FROM 1 FOR 2);
BEGIN
    IF NOT (p_delegate_id ~ '^\d+$' AND p_mandate_id ~ '^\d+$') THEN -- check for integer using regular expression
        RAISE EXCEPTION 'p_delegate_id and p_mandate_id must be integers';
    END IF;

    -- Get the representee ID from the code country and personal company code.
    SELECT id INTO v_representee_id
    FROM person
    WHERE personal_company_code_country = rpccc
        AND personal_company_code = rpcc;

    -- Set the deleted flag to true for the mandate matching the given IDs.
    UPDATE mandate
    SET deleted = TRUE
    WHERE id = CAST(p_mandate_id as INTEGER)
        AND representee_id = v_representee_id
        AND delegate_id = CAST(p_delegate_id AS INTEGER);
    IF FOUND THEN
          RETURN TRUE;
      ELSE
          RETURN FALSE;
      END IF;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION function_insert_mandate_subdelegate(
    p_sub_delegate_first_name TEXT,
    p_sub_delegate_surname TEXT,
    p_sub_delegate_type TEXT,
    p_sub_delegate_identifier TEXT,
    p_representee_identifier TEXT,
    p_delegate_identifier TEXT,
    p_mandate_identifier TEXT,
    p_validity_period_from DATE,
    p_validity_period_through DATE,
    p_created_by TEXT,
    p_created_by_represented_person TEXT,
    p_document_uuid TEXT,
    p_can_display_document_to_delegate BOOLEAN
) RETURNS BOOLEAN AS $$
BEGIN
    RETURN TRUE;
END;
$$ LANGUAGE plpgsql;