-- Prikazati sve session-e sa popunjenošću > 80%
SELECT
    s.session_id,
    s.start_time,
    s.end_time,
    t.name AS training_name,
    o.capacity,
    o.reserved_count,
    o.occupancy_percent
FROM sessions s
JOIN trainings t 
    ON t.training_id = s.training_id
CROSS JOIN LATERAL fn_session_occupancy(s.session_id) o
WHERE s.training_studio_id IS NOT NULL
  AND o.occupancy_percent > 80
ORDER BY o.occupancy_percent DESC;

-- prikazati sve session-e sa popunjenošću, sortirano po popunjenosti
SELECT
    s.session_id,
    s.start_time,
    s.end_time,
    t.name AS training_name,
    o.capacity,
    o.reserved_count,
    o.occupancy_percent
FROM sessions s
JOIN trainings t 
    ON t.training_id = s.training_id
CROSS JOIN LATERAL fn_session_occupancy(s.session_id) o
WHERE s.training_studio_id IS NOT NULL
ORDER BY o.occupancy_percent DESC;
-- LIMIT 5; -- samo top 5

-- test ako sve ima
SELECT * FROM fn_session_occupancy(34);
-- test ako session ima studio al nema rezervacije 
SELECT * FROM fn_session_occupancy(26);
-- test ako session nepostoji 
SELECT * FROM fn_session_occupancy(999);
-- test ako session postoji ali nema studija 
SELECT * FROM fn_session_occupancy(35); 
--  da ne broji cancelled rezervacije
SELECT COUNT(*) FROM reservations
WHERE session_id = 34 AND status='CANCELLED';

SELECT * FROM fn_session_occupancy(34);


-- ako promenimo rey na cancelled da se smanji procenat 
UPDATE reservations
SET status='CANCELLED'
WHERE reservation_id = 3
-- treba 2 session id da se smanji 
-- proveriti pre i posle
select * from fn_session_occupancy(2);


