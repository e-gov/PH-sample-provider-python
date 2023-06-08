CREATE OR REPLACE FUNCTION function_insert_mandate_subdelegate(

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
    p_created_by_represented_person TEXT,
    p_document_uuid TEXT,
    p_can_display_document_to_delegate BOOLEAN
) RETURNS BOOLEAN AS $$
BEGIN
RETURN TRUE;
END;
$$ LANGUAGE plpgsql;