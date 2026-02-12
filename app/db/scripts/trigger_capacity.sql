CREATE OR REPLACE FUNCTION trg_check_session_capacity()
RETURNS TRIGGER
LANGUAGE plpgsql
AS $$
DECLARE
    v_capacity INT;
    v_reserved_count INT;
    v_studio_id INT;
BEGIN
    -- Triger nas zanima samo kad status postaje RESERVED
    IF NEW.status <> 'RESERVED' THEN
        RETURN NEW;
    END IF;

    -- 1) Nađi session i studio_id
    SELECT s.training_studio_id
    INTO v_studio_id
    FROM sessions s
    WHERE s.session_id = NEW.session_id;

    IF NOT FOUND THEN
        RAISE EXCEPTION 'Session % ne postoji', NEW.session_id;
    END IF;

    -- 2) Ako session nema studio -> zabrani rezervaciju
    IF v_studio_id IS NULL THEN
        RAISE EXCEPTION 'Ne može rezervacija: session % nema dodeljen studio', NEW.session_id;
    END IF;

    -- 3) Uzmi kapacitet studija
    SELECT ts.capacity
    INTO v_capacity
    FROM training_studios ts
    WHERE ts.training_studio_id = v_studio_id;

    IF NOT FOUND OR v_capacity IS NULL THEN
        RAISE EXCEPTION 'Studio % ne postoji ili nema definisan kapacitet', v_studio_id;
    END IF;

    -- 4) Prebroj RESERVED rezervacije (pazi na UPDATE da ne broji samog sebe)
    SELECT COUNT(*)
    INTO v_reserved_count
    FROM reservations r
    WHERE r.session_id = NEW.session_id
      AND r.status = 'RESERVED'
      AND (TG_OP <> 'UPDATE' OR r.reservation_id <> OLD.reservation_id);

    -- 5) Ako bi prešlo kapacitet -> stop
    IF v_reserved_count >= v_capacity THEN
        RAISE EXCEPTION 'Nema slobodnih mesta: session %, capacity %, reserved %',
            NEW.session_id, v_capacity, v_reserved_count;
    END IF;

    RETURN NEW;
END;
$$;

-- Reinstalacija trigera (da možeš da rerunuješ skriptu koliko hoćeš)
DROP TRIGGER IF EXISTS check_session_capacity ON reservations;

CREATE TRIGGER check_session_capacity
BEFORE INSERT OR UPDATE OF status, session_id
ON reservations
FOR EACH ROW
EXECUTE FUNCTION trg_check_session_capacity();
