SELECT
    s.shop_name,
    COUNT(dr.delay_id) AS Total_Delays,
    SUM(dr.delay_minutes) AS Total_Delay_Minutes,
    ROUND(AVG(dr.delay_minutes),2) AS Average_Delay
FROM delay_records dr
JOIN shops s
ON dr.shop_id = s.shop_id
GROUP BY s.shop_name
ORDER BY Total_Delays DESC;
SELECT
    e.equipment_name,
    COUNT(dr.delay_id) AS Total_Delays,
    SUM(dr.delay_minutes) AS Total_Delay_Minutes,
    ROUND(AVG(dr.delay_minutes),2) AS Average_Delay
FROM delay_records dr
JOIN equipment e
ON dr.equipment_id = e.equipment_id
GROUP BY e.equipment_name
ORDER BY Total_Delays DESC;
SELECT
    a.agency_name,
    COUNT(dr.delay_id) AS Total_Delays,
    SUM(dr.delay_minutes) AS Total_Delay_Minutes,
    ROUND(AVG(dr.delay_minutes),2) AS Average_Delay
FROM delay_records dr
JOIN agencies a
ON dr.agency_id = a.agency_id
GROUP BY a.agency_name
ORDER BY Total_Delays DESC;
SELECT
    c.conveyor_name,
    COUNT(dr.delay_id) AS Total_Delays,
    SUM(dr.delay_minutes) AS Total_Delay_Minutes,
    ROUND(AVG(dr.delay_minutes),2) AS Average_Delay
FROM delay_records dr
JOIN conveyors c
ON dr.conveyor_id = c.conveyor_id
GROUP BY c.conveyor_name
ORDER BY Total_Delays DESC;
SELECT
    dt.delay_description,
    COUNT(dr.delay_id) AS Total_Delays,
    SUM(dr.delay_minutes) AS Total_Delay_Minutes,
    ROUND(AVG(dr.delay_minutes),2) AS Average_Delay
FROM delay_records dr
JOIN delay_types dt
ON dr.delay_type_id = dt.delay_type_id
GROUP BY dt.delay_description
ORDER BY Total_Delays DESC;
SELECT
    s.season_name,
    COUNT(dr.delay_id) AS Total_Delays,
    SUM(dr.delay_minutes) AS Total_Delay_Minutes,
    ROUND(AVG(dr.delay_minutes),2) AS Average_Delay
FROM delay_records dr
JOIN seasons s
ON dr.season_id = s.season_id
GROUP BY s.season_name
ORDER BY Total_Delays DESC;
SELECT
CASE
    WHEN delay_minutes < 30 THEN '0-30 Minutes'
    WHEN delay_minutes BETWEEN 30 AND 60 THEN '30-60 Minutes'
    WHEN delay_minutes BETWEEN 61 AND 120 THEN '1-2 Hours'
    ELSE 'More than 2 Hours'
END AS Duration_Category,
COUNT(*) AS Total_Delays
FROM delay_records
GROUP BY Duration_Category
ORDER BY Total_Delays DESC;