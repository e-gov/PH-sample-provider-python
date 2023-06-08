CREATE OR REPLACE FUNCTION function_create_mandate(
    p_representee_identifier TEXT,
    p_representee_first_name TEXT,
    p_representee_surname TEXT,
    p_representee_legal_name TEXT,
    p_representee_type TEXT,

    p_delegate_identifier TEXT,
    p_delegate_first_name TEXT,
    p_delegate_surname TEXT,
    p_delegate_legal_name TEXT,
    p_delegate_type TEXT,
    
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
    v_representee_id INTEGER;
    v_delegate_id INTEGER;

    v_representee_code TEXT := SUBSTRING(p_representee_identifier FROM 3);
    v_representee_country TEXT := SUBSTRING(p_representee_identifier FROM 1 FOR 2);

    v_delegate_code TEXT := SUBSTRING(p_delegate_identifier FROM 3);
    v_delegate_country TEXT := SUBSTRING(p_delegate_identifier FROM 1 FOR 2);

BEGIN

    -- Insert or update person record corresponding to representee
    INSERT INTO person (type, personal_company_code, personal_company_code_country, first_name, surname, legal_name)
    VALUES (p_representee_type, v_representee_code, v_representee_country, p_representee_first_name, p_representee_surname, p_representee_legal_name)
    ON CONFLICT (personal_company_code, personal_company_code_country)
        DO UPDATE SET first_name = EXCLUDED.first_name,
                      surname    = EXCLUDED.surname,
                      legal_name = EXCLUDED.legal_name
    RETURNING id INTO v_representee_id;
    
    -- Insert or update person record corresponding to delegate
    INSERT INTO person (type, personal_company_code, personal_company_code_country, first_name, surname, legal_name)
    VALUES (p_delegate_type, v_delegate_code, v_delegate_country, p_delegate_first_name, p_delegate_surname,  p_delegate_legal_name)
    ON CONFLICT (personal_company_code, personal_company_code_country)
        DO UPDATE SET first_name = EXCLUDED.first_name,
                      surname    = EXCLUDED.surname,
                      legal_name = EXCLUDED.legal_name
    RETURNING id INTO v_delegate_id;


-- Insert mandate record
    INSERT INTO mandate (representee_id, delegate_id, role, validity_period_from, validity_period_through,
                         can_sub_delegate, created_by, created_by_represented_person,
                         original_mandate_id, document_uuid, can_display_document_to_delegate)
    VALUES (v_representee_id, v_delegate_id, p_role, p_validity_period_from::DATE, p_validity_period_through::DATE,
            p_can_sub_delegate, p_created_by, p_created_by_represented_person,
            p_original_mandate_id, p_document_uuid, p_can_display_document_to_delegate);
END;
$$ LANGUAGE PLPGSQL;