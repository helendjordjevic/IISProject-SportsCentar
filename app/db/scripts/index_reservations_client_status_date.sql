CREATE INDEX idx_reservations_client_status_date
ON reservations (client_id, status, reservation_date DESC);

-- drop index za pre analizu
DROP INDEX IF EXISTS idx_reservations_client_status_date;

-- napraviti veliki broj sessiona za trening id 10, trening studio 6 
INSERT INTO sessions (start_time, end_time, training_id, training_studio_id, weekday, day_period)
SELECT
  NOW() + (gs || ' minutes')::interval,
  NOW() + ((gs + 45) || ' minutes')::interval,
  10,   -- training_id
  6,    -- training_studio_id
  'FRIDAY',
  'MORNING'
FROM generate_series(1, 20000) gs;

-- sve sessije se rezervisu od strane clienta 5
INSERT INTO reservations (client_id, session_id, reservation_date, status)
SELECT
  5 AS client_id,
  s.session_id,
  (CURRENT_DATE - (random()*365)::int) AS reservation_date,
  CASE 
    WHEN random() < 0.8 
    THEN 'RESERVED'::reservation_status_enum
    ELSE 'CANCELLED'::reservation_status_enum
  END
FROM (
  SELECT session_id
  FROM sessions
  WHERE training_id = 10 AND training_studio_id = 6
  ORDER BY session_id DESC
  LIMIT 20000
) s
ON CONFLICT (client_id, session_id) DO NOTHING;

-- upit za testiranje
EXPLAIN (ANALYZE, BUFFERS)
SELECT r.reservation_id, r.reservation_date, r.status
FROM reservations r
WHERE r.client_id = 5
  AND r.status = 'RESERVED'::reservation_status_enum
  AND r.reservation_date BETWEEN CURRENT_DATE - INTERVAL '180 days' AND CURRENT_DATE
ORDER BY r.reservation_date DESC;



