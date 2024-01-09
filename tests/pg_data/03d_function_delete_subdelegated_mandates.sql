CREATE OR REPLACE FUNCTION paasuke_delete_subdelegated_mandates(p_mandate_id TEXT)
RETURNS SETOF mandate AS $$
DECLARE
not_deleted_subdelegated_mandates_rows mandate;
BEGIN
    IF NOT (p_mandate_id ~ '^\d+$') THEN
        RAISE EXCEPTION 'p_mandate_id must be an integer';
END IF;

    -- Fetch the rows matching the given ID and conditions.
RETURN QUERY
SELECT *
FROM mandate
WHERE original_mandate_id = CAST(p_mandate_id AS INTEGER)
  AND (deleted = FALSE OR deleted IS NULL);

-- Update the rows matching the conditions to set the deleted flag to true.
UPDATE mandate
SET deleted = TRUE
WHERE original_mandate_id = CAST(p_mandate_id AS INTEGER)
  AND (deleted = FALSE OR deleted IS NULL);

-- If no rows were found, return an empty set.
RETURN;
END;
$$ LANGUAGE plpgsql;