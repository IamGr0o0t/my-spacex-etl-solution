--SQL Query to Find the Maximum Number of Times a Core Has Been Reused

SELECT 
    core_core, 
    MAX(core_flight) AS reuse_count
FROM 
    spacex_data
GROUP BY 
    core_core
ORDER BY 
    reuse_count DESC
--LIMIT 1

--SQL Query to Find the Cores that Have Been Reused in Less Than 50 Days After the Previous Launch
WITH core_launches AS (
    SELECT 
        c_core, 
        date_utc::timestamp AS launch_date,
        LAG(date_utc::timestamp) OVER (PARTITION BY c_core ORDER BY date_utc) AS previous_launch_date
    FROM 
        spacex_data
    WHERE 
        c_flight IS NOT NULL
)
SELECT 
    c_core, 
    launch_date, 
    previous_launch_date,
    DATE_DIFF('day', previous_launch_date, launch_date) AS days_between_launches
FROM 
    core_launches
WHERE 
    DATE_DIFF('day', previous_launch_date, launch_date) < 50
ORDER BY 
    days_between_launches ASC;


