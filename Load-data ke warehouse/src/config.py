"""
Configuration file untuk Data Warehouse Project
"""

import os
from pathlib import Path

# Project paths
PROJECT_ROOT = Path(__file__).parent.parent
DATA_DIR = PROJECT_ROOT / "data"
WAREHOUSE_DIR = PROJECT_ROOT / "warehouse"
SQL_DIR = PROJECT_ROOT / "sql"

# Database configuration
DATABASE_URL = f"sqlite:///{WAREHOUSE_DIR}/sensor_warehouse.db"
DATABASE_FILE = WAREHOUSE_DIR / "sensor_warehouse.db"

# Data source
CSV_FILE = "processed_sensor_data_20250930_092513.csv"
CSV_PATH = DATA_DIR / CSV_FILE

# Table names
FACT_TABLE = "fact_sensor_readings"
DIM_SENSOR_TABLE = "dim_sensors"
DIM_LOCATION_TABLE = "dim_locations"
DIM_TIME_TABLE = "dim_time"

# Batch processing
BATCH_SIZE = 1000

# Data quality thresholds
TEMPERATURE_MIN = -50.0
TEMPERATURE_MAX = 60.0
HUMIDITY_MIN = 0.0
HUMIDITY_MAX = 100.0
PRESSURE_MIN = 900.0
PRESSURE_MAX = 1100.0
AQI_MIN = 0.0
AQI_MAX = 500.0

print(f"Configuration loaded. Project root: {PROJECT_ROOT}")
print(f"CSV file path: {CSV_PATH}")
print(f"Database path: {DATABASE_FILE}")