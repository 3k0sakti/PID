#!/bin/bash

# ETL Pipeline Runner Script
# Run this script to execute the complete ETL pipeline

echo "🚀 Starting ETL Pipeline for Sensor Data Warehouse"
echo "=================================================="

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 is not installed. Please install Python3 first."
    exit 1
fi

echo "✅ Python3 found"

# Check if required directories exist
if [ ! -d "data" ]; then
    echo "❌ Data directory not found. Please ensure data/ directory exists."
    exit 1
fi

if [ ! -f "data/processed_sensor_data_20250930_092513.csv" ]; then
    echo "❌ Source CSV file not found in data/ directory."
    exit 1
fi

echo "✅ Data source found"

# Install dependencies
echo "📦 Installing dependencies..."
pip3 install -r requirements.txt

if [ $? -ne 0 ]; then
    echo "❌ Failed to install dependencies."
    exit 1
fi

echo "✅ Dependencies installed"

# Create warehouse directory if not exists
mkdir -p warehouse

# Run the ETL pipeline
echo "🔄 Running ETL Pipeline..."
python3 -c "
import sys
sys.path.append('./src')
from src.data_loader import DataLoader
from src.warehouse_manager import WarehouseManager
import time

print('📊 Starting ETL process...')
start_time = time.time()

# Initialize
loader = DataLoader()
warehouse = WarehouseManager()

try:
    # Extract
    print('📥 Extracting data...')
    data = loader.extract_data()
    
    # Transform
    print('🔄 Transforming data...')
    clean_data = loader.transform_data()
    
    # Load
    print('📤 Loading to warehouse...')
    loader.load_to_warehouse()
    
    end_time = time.time()
    print(f'✅ ETL completed in {end_time - start_time:.2f} seconds')
    
    # Show summary
    table_info = warehouse.get_table_info()
    print(f'📊 Warehouse Summary:')
    for table, info in table_info.items():
        print(f'  • {table}: {info[\"row_count\"]:,} records')
        
except Exception as e:
    print(f'❌ ETL failed: {e}')
    sys.exit(1)
finally:
    warehouse.close()

print('🎉 ETL Pipeline completed successfully!')
print('💡 Open hands_on_data_warehouse.ipynb for detailed analysis.')
"

echo "🎊 ETL Pipeline execution completed!"
echo "📓 Next steps:"
echo "  1. Open VS Code"
echo "  2. Open hands_on_data_warehouse.ipynb"
echo "  3. Run the notebook for detailed analysis"