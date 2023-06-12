CREATE OR REPLACE FUNCTION paasuke_add_mandate_subdelegate(
    p_representee_id TEXT,
    p_delegate_id TEXT,
    p_mandate_id TEXT,
    p_sub_delegate_identifier TEXT,
    p_sub_delegate_first_name TEXT,
    p_sub_delegate_surname TEXT,
    p_sub_delegate_legal_name TEXT,
    p_sub_delegate_type TEXT,
    p_validity_period_from DATE,
    p_validity_period_through DATE,
    p_created_by TEXT,
    p_document_uuid TEXT,
    p_can_display_document_to_delegate BOOLEAN
) RETURNS BOOLEAN AS
$$
DECLARE
    rec_existing_mandate mandate%ROWTYPE;
    v_sub_delegate_code TEXT := SUBSTRING(p_sub_delegate_identifier FROM 3);
    v_sub_delegate_country TEXT := SUBSTRING(p_sub_delegate_identifier FROM 1 FOR 2);

    v_sub_delegate_id person.id%TYPE;

    v_representee_id person.id%TYPE := p_representee_id::integer;
    v_delegate_id person.id%TYPE := p_delegate_id::integer;
    v_mandate_id mandate.id%TYPE := p_mandate_id::integer;
    v_validity_period_from mandate.validity_period_from%TYPE := p_validity_period_from;

BEGIN
        SELECT *
        INTO rec_existing_mandate
        FROM mandate
        WHERE representee_id = v_representee_id
          AND delegate_id = v_delegate_id
          AND id = v_mandate_id;

    IF rec_existing_mandate.id IS NULL THEN
        RAISE 'There is no mandate where id=% AND representee_id=% AND delegate_id=%', p_mandate_id, v_representee_id, v_delegate_id USING ERRCODE = '23002';
    end if;

    IF rec_existing_mandate.can_sub_delegate = FALSE THEN
        RAISE 'Mandate to sub-delegate (id=%) has can_sub_delegate=FALSE', p_mandate_id USING ERRCODE = '23002';
    end if;

    IF p_validity_period_from IS NULL THEN
        v_validity_period_from := NOW();
    end if;

    IF p_validity_period_through IS NOT NULL AND v_validity_period_from > p_validity_period_through THEN
        RAISE 'Mandate to sub-delegate (id=%) has validity_period_through before validity_period_from', p_mandate_id USING ERRCODE = '23003';
    end if;

    IF rec_existing_mandate.validity_period_from > v_validity_period_from THEN
        RAISE 'Mandate to sub-delegate (id=%) has validity_period_from=% BUT new mandate is set to start=% (which is earlier)',
            p_mandate_id,
            rec_existing_mandate.validity_period_from,
            v_validity_period_from
            USING ERRCODE = '23004';
    end if;

    IF p_validity_period_through IS NULL AND rec_existing_mandate.validity_period_through IS NOT NULL THEN
        RAISE 'Mandate to sub-delegate (id=%) has validity_period_through=% BUT new mandate is set to be valid indefinitely (which is longer)',
            p_mandate_id,
            rec_existing_mandate.validity_period_through
            USING ERRCODE = '23005';
    end if;

    -- Insert or update person record corresponding to new delegate
    INSERT INTO person (type, personal_company_code, personal_company_code_country, first_name, surname, legal_name)
    VALUES (p_sub_delegate_type, v_sub_delegate_code, v_sub_delegate_country, p_sub_delegate_first_name, p_sub_delegate_surname, p_sub_delegate_legal_name)
    ON CONFLICT (personal_company_code, personal_company_code_country)
        DO UPDATE SET first_name = EXCLUDED.first_name,
                      surname    = EXCLUDED.surname,
                      legal_name = EXCLUDED.legal_name
    RETURNING id INTO v_sub_delegate_id;


    INSERT INTO mandate (representee_id, delegate_id, role, validity_period_from, validity_period_through,
                         can_sub_delegate, created_by,  original_mandate_id)
    VALUES (v_representee_id, v_sub_delegate_id, rec_existing_mandate.role, v_validity_period_from::DATE, p_validity_period_through::DATE,
            FALSE, p_created_by, rec_existing_mandate.id);

    RETURN TRUE;
END;
$$ LANGUAGE plpgsql;