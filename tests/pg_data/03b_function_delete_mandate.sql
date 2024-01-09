CREATE OR REPLACE FUNCTION paasuke_delete_mandate(
    p_representee_id INT,
    p_delegate_id INT,
    p_mandate_id TEXT
) RETURNS BOOLEAN AS $$
BEGIN
    IF NOT (p_mandate_id ~ '^\d+$') THEN
        RAISE EXCEPTION 'p_mandate_id must be integer';
END IF;


-- Set the deleted flag to true for the mandate matching the given IDs.
UPDATE mandate
  SET deleted = TRUE
WHERE id = CAST(p_mandate_id as INTEGER)
  AND representee_id = CAST(p_representee_id AS INTEGER)
  AND delegate_id = CAST(p_delegate_id AS INTEGER);
IF FOUND THEN
          RETURN TRUE;
ELSE
          RETURN FALSE;
END IF;
END;
$$ LANGUAGE plpgsql;