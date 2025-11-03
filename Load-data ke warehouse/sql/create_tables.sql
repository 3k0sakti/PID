-- DDL Scripts for Sensor Data Warehouse
-- Created: October 2025

-- ================================
-- DIMENSION TABLES
-- ================================

-- Dimension: Sensors
CREATE TABLE IF NOT EXISTS dim_sensors (
    sensor_key INTEGER PRIMARY KEY AUTOINCREMENT,
    sensor_id VARCHAR(50) UNIQUE NOT NULL,
    status VARCHAR(20),
    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Dimension: Locations
CREATE TABLE IF NOT EXISTS dim_locations (
    location_key INTEGER PRIMARY KEY AUTOINCREMENT,
    location_name VARCHAR(100) UNIQUE NOT NULL,
    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Dimension: Time
CREATE TABLE IF NOT EXISTS dim_time (
    time_key INTEGER PRIMARY KEY AUTOINCREMENT,
    full_date DATE UNIQUE NOT NULL,
    year INTEGER,
    month INTEGER,
    day INTEGER,
    hour INTEGER,
    day_of_week INTEGER,
    is_weekend BOOLEAN,
    time_period VARCHAR(20),
    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ================================
-- FACT TABLE
-- ================================

-- Fact Table: Sensor Readings
CREATE TABLE IF NOT EXISTS fact_sensor_readings (
    reading_id INTEGER PRIMARY KEY AUTOINCREMENT,
    sensor_key INTEGER,
    location_key INTEGER,
    time_key INTEGER,
    timestamp TIMESTAMP,
    
    -- Core measurements
    temperature_celsius REAL,
    humidity_percent REAL,
    pressure_hpa REAL,
    air_quality_aqi REAL,
    
    -- Derived measurements
    temperature_fahrenheit REAL,
    temperature_kelvin REAL,
    heat_index_f REAL,
    heat_index_c REAL,
    aqi_category VARCHAR(20),
    comfort_index REAL,
    
    -- Normalized values
    temperature_celsius_normalized REAL,
    humidity_percent_normalized REAL,
    pressure_hpa_normalized REAL,
    air_quality_aqi_normalized REAL,
    
    -- Metadata
    load_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- Foreign key constraints
    FOREIGN KEY (sensor_key) REFERENCES dim_sensors(sensor_key),
    FOREIGN KEY (location_key) REFERENCES dim_locations(location_key),
    FOREIGN KEY (time_key) REFERENCES dim_time(time_key)
);

-- ================================
-- INDEXES
-- ================================

-- Fact table indexes for performance
CREATE INDEX IF NOT EXISTS idx_fact_timestamp ON fact_sensor_readings(timestamp);
CREATE INDEX IF NOT EXISTS idx_fact_sensor_key ON fact_sensor_readings(sensor_key);
CREATE INDEX IF NOT EXISTS idx_fact_location_key ON fact_sensor_readings(location_key);
CREATE INDEX IF NOT EXISTS idx_fact_time_key ON fact_sensor_readings(time_key);
CREATE INDEX IF NOT EXISTS idx_fact_date_sensor ON fact_sensor_readings(timestamp, sensor_key);

-- Dimension table indexes
CREATE INDEX IF NOT EXISTS idx_sensor_id ON dim_sensors(sensor_id);
CREATE INDEX IF NOT EXISTS idx_location_name ON dim_locations(location_name);
CREATE INDEX IF NOT EXISTS idx_time_date ON dim_time(full_date);
CREATE INDEX IF NOT EXISTS idx_time_year_month ON dim_time(year, month);

-- ================================
-- VIEWS FOR ANALYTICS
-- ================================

-- View: Complete sensor readings with dimension details
CREATE VIEW IF NOT EXISTS vw_sensor_readings_complete AS
SELECT 
    f.reading_id,
    f.timestamp,
    s.sensor_id,
    l.location_name,
    t.year,
    t.month,
    t.day,
    t.hour,
    t.day_of_week,
    t.is_weekend,
    t.time_period,
    f.temperature_celsius,
    f.humidity_percent,
    f.pressure_hpa,
    f.air_quality_aqi,
    f.temperature_fahrenheit,
    f.aqi_category,
    f.comfort_index
FROM fact_sensor_readings f
JOIN dim_sensors s ON f.sensor_key = s.sensor_key
JOIN dim_locations l ON f.location_key = l.location_key
JOIN dim_time t ON f.time_key = t.time_key;

-- View: Daily aggregated sensor data
CREATE VIEW IF NOT EXISTS vw_daily_sensor_summary AS
SELECT 
    DATE(f.timestamp) as date,
    s.sensor_id,
    l.location_name,
    COUNT(*) as reading_count,
    AVG(f.temperature_celsius) as avg_temperature,
    MIN(f.temperature_celsius) as min_temperature,
    MAX(f.temperature_celsius) as max_temperature,
    AVG(f.humidity_percent) as avg_humidity,
    AVG(f.pressure_hpa) as avg_pressure,
    AVG(f.air_quality_aqi) as avg_aqi
FROM fact_sensor_readings f
JOIN dim_sensors s ON f.sensor_key = s.sensor_key
JOIN dim_locations l ON f.location_key = l.location_key
GROUP BY DATE(f.timestamp), s.sensor_id, l.location_name;

-- View: Location-based aggregations
CREATE VIEW IF NOT EXISTS vw_location_summary AS
SELECT 
    l.location_name,
    COUNT(DISTINCT s.sensor_id) as sensor_count,
    COUNT(f.reading_id) as total_readings,
    AVG(f.temperature_celsius) as avg_temperature,
    AVG(f.humidity_percent) as avg_humidity,
    AVG(f.air_quality_aqi) as avg_aqi,
    MIN(f.timestamp) as first_reading,
    MAX(f.timestamp) as last_reading
FROM fact_sensor_readings f
JOIN dim_sensors s ON f.sensor_key = s.sensor_key
JOIN dim_locations l ON f.location_key = l.location_key
GROUP BY l.location_name;