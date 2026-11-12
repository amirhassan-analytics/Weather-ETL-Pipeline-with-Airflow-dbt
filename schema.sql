-- Weather star schema (PostgreSQL).
CREATE TABLE IF NOT EXISTS staging_weather (
    timestamp TIMESTAMP,
    temperature_2m NUMERIC,
    relative_humidity_2m NUMERIC,
    precipitation NUMERIC,
    wind_speed_10m NUMERIC,
    city TEXT,
    latitude NUMERIC,
    longitude NUMERIC,
    date DATE
);

CREATE TABLE IF NOT EXISTS dim_location (
    city TEXT PRIMARY KEY,
    latitude NUMERIC,
    longitude NUMERIC
);

CREATE TABLE IF NOT EXISTS dim_date (
    date DATE PRIMARY KEY,
    year INT,
    month INT,
    day INT
);
