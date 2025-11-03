-- Sample Analytics Queries for Sensor Data Warehouse
-- Created: October 2025

-- ================================
-- BASIC DATA EXPLORATION
-- ================================

-- 1. Total records and data overview
SELECT 
    'Sensors' as table_name, COUNT(*) as record_count 
FROM dim_sensors
UNION ALL
SELECT 
    'Locations' as table_name, COUNT(*) as record_count 
FROM dim_locations
UNION ALL
SELECT 
    'Time Periods' as table_name, COUNT(*) as record_count 
FROM dim_time
UNION ALL
SELECT 
    'Sensor Readings' as table_name, COUNT(*) as record_count 
FROM fact_sensor_readings;

-- 2. Data quality check - completeness
SELECT 
    'Temperature' as metric,
    COUNT(*) as total_records,
    COUNT(temperature_celsius) as non_null_records,
    ROUND(COUNT(temperature_celsius) * 100.0 / COUNT(*), 2) as completeness_percent
FROM fact_sensor_readings
UNION ALL
SELECT 
    'Humidity' as metric,
    COUNT(*) as total_records,
    COUNT(humidity_percent) as non_null_records,
    ROUND(COUNT(humidity_percent) * 100.0 / COUNT(*), 2) as completeness_percent
FROM fact_sensor_readings
UNION ALL
SELECT 
    'Air Quality' as metric,
    COUNT(*) as total_records,
    COUNT(air_quality_aqi) as non_null_records,
    ROUND(COUNT(air_quality_aqi) * 100.0 / COUNT(*), 2) as completeness_percent
FROM fact_sensor_readings;

-- ================================
-- TEMPORAL ANALYSIS
-- ================================

-- 3. Readings by time period
SELECT 
    t.time_period,
    COUNT(*) as reading_count,
    AVG(f.temperature_celsius) as avg_temperature,
    AVG(f.humidity_percent) as avg_humidity,
    AVG(f.air_quality_aqi) as avg_aqi
FROM fact_sensor_readings f
JOIN dim_time t ON f.time_key = t.time_key
GROUP BY t.time_period
ORDER BY 
    CASE t.time_period 
        WHEN 'Night' THEN 1
        WHEN 'Morning' THEN 2
        WHEN 'Afternoon' THEN 3
        WHEN 'Evening' THEN 4
        ELSE 5
    END;

-- 4. Daily trend analysis (first 7 days)
SELECT 
    DATE(f.timestamp) as date,
    t.day_of_week,
    CASE t.day_of_week
        WHEN 0 THEN 'Monday'
        WHEN 1 THEN 'Tuesday'
        WHEN 2 THEN 'Wednesday'
        WHEN 3 THEN 'Thursday'
        WHEN 4 THEN 'Friday'
        WHEN 5 THEN 'Saturday'
        WHEN 6 THEN 'Sunday'
    END as day_name,
    COUNT(*) as reading_count,
    ROUND(AVG(f.temperature_celsius), 2) as avg_temperature,
    ROUND(AVG(f.humidity_percent), 2) as avg_humidity,
    ROUND(AVG(f.air_quality_aqi), 2) as avg_aqi
FROM fact_sensor_readings f
JOIN dim_time t ON f.time_key = t.time_key
GROUP BY DATE(f.timestamp), t.day_of_week
ORDER BY DATE(f.timestamp)
LIMIT 7;

-- 5. Weekend vs Weekday comparison
SELECT 
    CASE WHEN t.is_weekend = 1 THEN 'Weekend' ELSE 'Weekday' END as period_type,
    COUNT(*) as reading_count,
    ROUND(AVG(f.temperature_celsius), 2) as avg_temperature,
    ROUND(AVG(f.humidity_percent), 2) as avg_humidity,
    ROUND(AVG(f.air_quality_aqi), 2) as avg_aqi,
    ROUND(MIN(f.temperature_celsius), 2) as min_temperature,
    ROUND(MAX(f.temperature_celsius), 2) as max_temperature
FROM fact_sensor_readings f
JOIN dim_time t ON f.time_key = t.time_key
GROUP BY t.is_weekend;

-- ================================
-- LOCATION-BASED ANALYSIS
-- ================================

-- 6. Location performance summary
SELECT 
    l.location_name,
    COUNT(DISTINCT s.sensor_id) as active_sensors,
    COUNT(*) as total_readings,
    ROUND(AVG(f.temperature_celsius), 2) as avg_temperature,
    ROUND(AVG(f.humidity_percent), 2) as avg_humidity,
    ROUND(AVG(f.air_quality_aqi), 2) as avg_aqi,
    f.aqi_category as dominant_aqi_category
FROM fact_sensor_readings f
JOIN dim_sensors s ON f.sensor_key = s.sensor_key
JOIN dim_locations l ON f.location_key = l.location_key
GROUP BY l.location_name, f.aqi_category
ORDER BY l.location_name, COUNT(*) DESC;

-- 7. Best and worst air quality locations
SELECT 
    'Best Air Quality' as category,
    l.location_name,
    ROUND(AVG(f.air_quality_aqi), 2) as avg_aqi,
    COUNT(*) as reading_count
FROM fact_sensor_readings f
JOIN dim_locations l ON f.location_key = l.location_key
GROUP BY l.location_name
ORDER BY AVG(f.air_quality_aqi) ASC
LIMIT 3

UNION ALL

SELECT 
    'Worst Air Quality' as category,
    l.location_name,
    ROUND(AVG(f.air_quality_aqi), 2) as avg_aqi,
    COUNT(*) as reading_count
FROM fact_sensor_readings f
JOIN dim_locations l ON f.location_key = l.location_key
GROUP BY l.location_name
ORDER BY AVG(f.air_quality_aqi) DESC
LIMIT 3;

-- ================================
-- SENSOR ANALYSIS
-- ================================

-- 8. Sensor performance and reliability
SELECT 
    s.sensor_id,
    l.location_name,
    s.status,
    COUNT(*) as reading_count,
    ROUND(AVG(f.temperature_celsius), 2) as avg_temperature,
    ROUND(AVG(f.humidity_percent), 2) as avg_humidity,
    ROUND(AVG(f.air_quality_aqi), 2) as avg_aqi,
    MIN(f.timestamp) as first_reading,
    MAX(f.timestamp) as last_reading
FROM fact_sensor_readings f
JOIN dim_sensors s ON f.sensor_key = s.sensor_key
JOIN dim_locations l ON f.location_key = l.location_key
GROUP BY s.sensor_id, l.location_name, s.status
ORDER BY reading_count DESC;

-- 9. Sensors with unusual readings (outliers)
SELECT 
    s.sensor_id,
    l.location_name,
    COUNT(*) as unusual_readings,
    ROUND(AVG(f.temperature_celsius), 2) as avg_temp,
    ROUND(AVG(f.humidity_percent), 2) as avg_humidity
FROM fact_sensor_readings f
JOIN dim_sensors s ON f.sensor_key = s.sensor_key
JOIN dim_locations l ON f.location_key = l.location_key
WHERE 
    f.temperature_celsius > 50 OR f.temperature_celsius < -10 OR
    f.humidity_percent > 95 OR f.humidity_percent < 5
GROUP BY s.sensor_id, l.location_name
ORDER BY unusual_readings DESC;

-- ================================
-- CORRELATION AND PATTERNS
-- ================================

-- 10. Temperature vs Air Quality correlation by location
SELECT 
    l.location_name,
    ROUND(AVG(f.temperature_celsius), 2) as avg_temperature,
    ROUND(AVG(f.air_quality_aqi), 2) as avg_aqi,
    COUNT(*) as sample_size,
    CASE 
        WHEN AVG(f.temperature_celsius) > 30 AND AVG(f.air_quality_aqi) > 100 THEN 'High Temp, Poor Air'
        WHEN AVG(f.temperature_celsius) > 30 AND AVG(f.air_quality_aqi) <= 50 THEN 'High Temp, Good Air'
        WHEN AVG(f.temperature_celsius) <= 20 AND AVG(f.air_quality_aqi) > 100 THEN 'Low Temp, Poor Air'
        WHEN AVG(f.temperature_celsius) <= 20 AND AVG(f.air_quality_aqi) <= 50 THEN 'Low Temp, Good Air'
        ELSE 'Moderate'
    END as environmental_category
FROM fact_sensor_readings f
JOIN dim_locations l ON f.location_key = l.location_key
GROUP BY l.location_name
ORDER BY avg_aqi DESC;

-- ================================
-- TIME SERIES ANALYSIS
-- ================================

-- 11. Hourly patterns (average by hour of day)
SELECT 
    t.hour,
    COUNT(*) as reading_count,
    ROUND(AVG(f.temperature_celsius), 2) as avg_temperature,
    ROUND(AVG(f.humidity_percent), 2) as avg_humidity,
    ROUND(AVG(f.air_quality_aqi), 2) as avg_aqi
FROM fact_sensor_readings f
JOIN dim_time t ON f.time_key = t.time_key
GROUP BY t.hour
ORDER BY t.hour;

-- 12. Data availability timeline
SELECT 
    DATE(f.timestamp) as date,
    COUNT(*) as readings_per_day,
    COUNT(DISTINCT s.sensor_id) as active_sensors,
    COUNT(DISTINCT l.location_name) as active_locations
FROM fact_sensor_readings f
JOIN dim_sensors s ON f.sensor_key = s.sensor_key
JOIN dim_locations l ON f.location_key = l.location_key
GROUP BY DATE(f.timestamp)
ORDER BY DATE(f.timestamp)
LIMIT 10;

-- ================================
-- ADVANCED ANALYTICS
-- ================================

-- 13. Moving average temperature by location (3-hour window)
WITH hourly_temps AS (
    SELECT 
        l.location_name,
        DATE(f.timestamp) as date,
        t.hour,
        AVG(f.temperature_celsius) as hourly_avg_temp
    FROM fact_sensor_readings f
    JOIN dim_locations l ON f.location_key = l.location_key
    JOIN dim_time t ON f.time_key = t.time_key
    GROUP BY l.location_name, DATE(f.timestamp), t.hour
)
SELECT 
    location_name,
    date,
    hour,
    ROUND(hourly_avg_temp, 2) as temperature,
    ROUND(AVG(hourly_avg_temp) OVER (
        PARTITION BY location_name 
        ORDER BY date, hour 
        ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
    ), 2) as moving_avg_3h
FROM hourly_temps
ORDER BY location_name, date, hour
LIMIT 50;

-- 14. AQI category distribution
SELECT 
    aqi_category,
    COUNT(*) as count,
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM fact_sensor_readings), 2) as percentage
FROM fact_sensor_readings
WHERE aqi_category IS NOT NULL
GROUP BY aqi_category
ORDER BY count DESC;