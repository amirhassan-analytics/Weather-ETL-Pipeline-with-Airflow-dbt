-- Staging model: one clean row per city per hour.
SELECT
    city,
    timestamp,
    date,
    temperature_2m,
    relative_humidity_2m,
    precipitation,
    wind_speed_10m
FROM {{ source('weather', 'staging_weather') }}
WHERE city IS NOT NULL
  AND timestamp IS NOT NULL
