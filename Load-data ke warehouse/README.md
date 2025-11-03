# Hands-on: Load Data ke Data Warehouse

## Overview
Tutorial ini akan memandu Anda melalui proses loading data sensor ke data warehouse menggunakan Python dan SQLite sebagai simulasi warehouse.

## Dataset
Data yang digunakan adalah data sensor IoT dengan informasi:
- **File**: `processed_sensor_data_20250930_092513.csv`
- **Jumlah Records**: ~28,816 rows
- **Columns**: 25 kolom termasuk timestamp, sensor_id, location, temperature, humidity, pressure, air quality, dll.

## Struktur Tutorial
1. **Data Exploration & Validation**
2. **Database Schema Design**
3. **ETL Pipeline Implementation**
4. **Data Loading & Verification**
5. **Query Examples & Analytics**

## Prerequisites
- Python 3.8+
- pandas
- sqlite3
- sqlalchemy
- numpy

## Getting Started
1. Install dependencies: `pip install -r requirements.txt`
2. Jalankan notebook: `jupyter notebook hands_on_data_warehouse.ipynb`
3. Ikuti langkah-langkah dalam notebook

## File Structure
```
├── README.md                              # Dokumentasi ini
├── requirements.txt                       # Python dependencies
├── hands_on_data_warehouse.ipynb         # Main tutorial notebook
├── src/
│   ├── __init__.py
│   ├── data_loader.py                     # ETL pipeline
│   ├── warehouse_manager.py               # Database operations
│   └── config.py                          # Configuration
├── sql/
│   ├── create_tables.sql                  # DDL scripts
│   └── sample_queries.sql                 # Sample analytics queries
├── data/
│   └── processed_sensor_data_*.csv        # Raw data
└── warehouse/
    └── sensor_warehouse.db                # SQLite database (akan dibuat)
```

## Learning Objectives
Setelah menyelesaikan tutorial ini, Anda akan dapat:
- Memahami konsep data warehouse dan ETL
- Merancang schema untuk time-series data
- Mengimplementasikan ETL pipeline dengan Python
- Melakukan data validation dan quality checks
- Mengoptimalkan query untuk analytics
- Memahami best practices untuk data warehousing