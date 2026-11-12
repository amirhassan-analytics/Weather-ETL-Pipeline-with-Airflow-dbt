-- Mart: daily weather per city — feeds dashboards and reports.
SELECT
    city,
    date,
    AVG(temperature_2m) AS avg_temperature,
    MIN(temperature_2m) AS min_temperature,
    MAX(temperature_2m) AS max_temperature,
    AVG(relative_humidity_2m) AS avg_humidity,
    SUM(precipitation) AS total_precipitation,
    AVG(wind_speed_10m) AS avg_wind_speed,
    COUNT(*) AS hours_recorded
FROM {{ ref('staging_weather') }}
GROUP BY city, date
