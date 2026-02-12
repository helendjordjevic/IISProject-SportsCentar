CREATE OR REPLACE FUNCTION fn_session_occupancy(p_session_id INT)
RETURNS TABLE (
    session_id INT,
    studio_id INT,
    capacity INT,
    reserved_count INT,
    occupancy_percent NUMERIC
)
LANGUAGE plpgsql
AS $$
DECLARE
    v_studio_id INT;
    v_capacity INT;
    v_reserved INT;
BEGIN
    -- proveriti dal session postoji 
    SELECT s.training_studio_id
    INTO v_studio_id
    FROM sessions s
    WHERE s.session_id = p_session_id;

    IF NOT FOUND THEN
        RAISE EXCEPTION 'Session % ne postoji', p_session_id;
    END IF;

    -- da li session ima training_studio_id?
    IF v_studio_id IS NULL THEN
        RAISE EXCEPTION 'Session % nema dodeljen studio', p_session_id;
    END IF;

    -- ako studio nepostoji ili nema odredjen kapacitet
    SELECT ts.capacity
    INTO v_capacity
    FROM training_studios ts
    WHERE ts.training_studio_id = v_studio_id;

    IF NOT FOUND OR v_capacity IS NULL THEN
        RAISE EXCEPTION 'Studio % ne postoji ili nema kapacitet', v_studio_id;
    END IF;

    -- prebroj reserved
    SELECT COUNT(*)
    INTO v_reserved
    FROM reservations r
    WHERE r.session_id = p_session_id
      AND r.status = 'RESERVED';

    RETURN QUERY
    SELECT
        p_session_id,
        v_studio_id,
        v_capacity,
        v_reserved,
        ROUND((v_reserved::NUMERIC / v_capacity::NUMERIC) * 100, 2);

END;
$$;
