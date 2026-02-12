-- jedan red u izvestaju ce da izgleda:

CREATE TYPE instructor_report_row AS (
    instructor_id INT,
    instructor_name TEXT,
    training_id INT,
    training_name TEXT,
    sessions_count INT,
    reserved_count INT,
    attended_count INT,
    attendance_rate NUMERIC,
    avg_rating NUMERIC
);

-- ako zelimo da pretrazimo za jednog ili vise instruktora, a ako prosledimo praznu listu onda daje sve instruktore
CREATE TYPE instructor_filter AS (
    instructor_ids INT[]
);

-- funkcija koja generise ceo izvestaj (koristim cursor, with, join, group by + having)
-- vraca set instructor report row
CREATE OR REPLACE FUNCTION fn_instructor_performance_report(
    p_date_from DATE, -- period izvestaja
    p_date_to DATE, 
    p_filter instructor_filter DEFAULT NULL,
    p_min_reserved INT DEFAULT 3
)
RETURNS SETOF instructor_report_row
LANGUAGE plpgsql
AS $$
DECLARE
    rec instructor_report_row;
    cur REFCURSOR; -- kursor - on iterira kroz rez upita
BEGIN
    -- izvrsi select ali red po red
    OPEN cur FOR
    WITH -- secemo odma podatke koji su nam potrebni za izvestaj, da ne bi posle u joinovima i grupisanju radili sa velikim tabelama
    base_sessions AS ( -- privremena tabela koja sadrzi samo sesije koje su u periodu i koje su vezane za instruktora koje zelimo da vidimo u izvestaju
        SELECT
            s.session_id,
            s.training_id,
            t.instructor_id,
            s.start_time::date AS session_date
        FROM sessions s
        JOIN trainings t ON t.training_id = s.training_id
        WHERE s.start_time::date BETWEEN p_date_from AND p_date_to
          AND (p_filter IS NULL OR t.instructor_id = ANY(p_filter.instructor_ids))
    ),
    agg AS ( -- pa onda grupisemo po instruktoru i treningu da dobijemo broj sesija, rezervacija, prisustava i prosecnu ocenu
        SELECT
            u.user_id AS instructor_id,
            (u.first_name || ' ' || u.last_name) AS instructor_name,
            tr.training_id,
            tr.name AS training_name,

            COUNT(DISTINCT bs.session_id) AS sessions_count, -- Broji koliko različitih session-a postoji za taj trening u periodu.

            COUNT(DISTINCT r.reservation_id) FILTER (WHERE r.status = 'RESERVED'::reservation_status_enum) AS reserved_count, -- Broji koliko rezervacija je RESERVED (aktivnih) za te session-e

            COUNT(DISTINCT a.attendance_id) FILTER (WHERE a.attendance_status = 'ATTENDED'::attendance_status_enum) AS attended_count, -- Broji koliko je dolazaka (attendance) gde je status ATTENDED.

            AVG(a.training_rating) FILTER (WHERE a.training_rating IS NOT NULL) AS avg_rating -- Prosečna ocena treninga (ignoriše NULL).

        FROM base_sessions bs
        JOIN trainings tr ON tr.training_id = bs.training_id
        JOIN users u ON u.user_id = bs.instructor_id

        LEFT JOIN reservations r ON r.session_id = bs.session_id
        LEFT JOIN attendances a ON a.session_id = bs.session_id

        WHERE u.user_type = 'INSTRUCTOR'::user_type_enum
        GROUP BY u.user_id, u.first_name, u.last_name, tr.training_id, tr.name -- group za count i avg

        HAVING COUNT(DISTINCT r.reservation_id) FILTER (WHERE r.status = 'RESERVED'::reservation_status_enum) >= p_min_reserved -- uslov da se ukljuce samo oni instruktori koji imaju bar p_min_reserved rezervacija
    )
    -- izracunavanje attendance_rate i formatiranje avg_rating, i sortiranje po attendance_rate i avg_rating
    SELECT
        instructor_id,
        instructor_name,
        training_id,
        training_name,
        sessions_count,
        reserved_count,
        attended_count,
        CASE
            WHEN reserved_count = 0 THEN 0
            ELSE ROUND((attended_count::NUMERIC / reserved_count::NUMERIC) * 100, 2) -- attendance_rate kao procenat, zaokruzen na 2 decimale, bez deljenja sa nulom
        END AS attendance_rate,
        ROUND(COALESCE(avg_rating, 0)::NUMERIC, 2) AS avg_rating -- ako nema rating onda 0 svakako
    FROM agg
    ORDER BY attendance_rate DESC, avg_rating DESC;

    LOOP
        FETCH cur INTO rec; -- sledeci red iz kursora
        EXIT WHEN NOT FOUND; -- ako nema vise redova, izlazi iz petlje
        RETURN NEXT rec; -- dodaj taj red u rezultat 
    END LOOP; 

    CLOSE cur;
END;
$$;

