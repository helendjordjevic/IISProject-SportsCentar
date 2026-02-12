-- upiti
-- poslednjih 180 dana, bez filtera
SELECT *
FROM fn_instructor_performance_report(
  CURRENT_DATE - 180,
  CURRENT_DATE,
  NULL::instructor_filter,
  1
)
LIMIT 20;

-- prag za having koliki da bude 
-- top treningi po broju RESERVED u periodu (da znaš šta je realno)
SELECT t.instructor_id, t.training_id, t.name,
       COUNT(*) FILTER (WHERE r.status='RESERVED'::reservation_status_enum) AS reserved_cnt
FROM sessions s
JOIN trainings t ON t.training_id=s.training_id
LEFT JOIN reservations r ON r.session_id=s.session_id
WHERE s.start_time::date BETWEEN CURRENT_DATE - 180 AND CURRENT_DATE
GROUP BY t.instructor_id, t.training_id, t.name
ORDER BY reserved_cnt DESC
LIMIT 10;

--  u poslednjih 180 dana za instruktore koji imaju preko 50 rez
SELECT *
FROM fn_instructor_performance_report(
  CURRENT_DATE - 180,
  CURRENT_DATE,
  NULL::instructor_filter,
  50
);

-- po jednom instruktoru ili vide 
SELECT *
FROM fn_instructor_performance_report(
  CURRENT_DATE - 180,
  CURRENT_DATE,
  ROW(ARRAY[9, 2])::instructor_filter,
  1
);



