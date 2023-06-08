CREATE OR REPLACE FUNCTION function_delete_mandate(
    p_representee_id TEXT,
    p_delegate_id TEXT,
    p_mandate_id TEXT
) RETURNS BOOLEAN AS $$
BEGIN
    IF NOT (p_representee_id ~ '^\d+$' AND p_delegate_id ~ '^\d+$' AND p_mandate_id ~ '^\d+$') THEN
        RAISE EXCEPTION 'p_representee_id, p_delegate_id and p_mandate_id must be integers';
END IF;


-- Set the deleted flag to true for the mandate matching the given IDs.
UPDATE mandate
  SET deleted = TRUE
WHERE id = CAST(p_mandate_id as INTEGER)
  AND representee_id = p_representee_id
  AND delegate_id = CAST(p_delegate_id AS INTEGER);
IF FOUND THEN
          RETURN TRUE;
ELSE
          RETURN FALSE;
END IF;
END;
$$ LANGUAGE plpgsql;