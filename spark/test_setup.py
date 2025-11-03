import json
import time
from datetime import datetime

# Quick test to verify the project structure works
print("IoT Streaming Pipeline - Quick Test")
print("=" * 50)

# Test 1: Check if Kafka is accessible
print("\n1. Testing Kafka connectivity...")
try:
    from kafka import KafkaProducer
    from kafka.errors import KafkaError
    
    producer = KafkaProducer(
        bootstrap_servers='localhost:9092',
        value_serializer=lambda v: json.dumps(v).encode('utf-8'),
        request_timeout_ms=5000,
    )
    
    # Send test message
    test_msg = {
        "device_id": "test-device",
        "ts": int(time.time() * 1000),
        "temperature": 25.0,
        "humidity": 60.0,
        "battery": 100.0,
        "status": "ok",
        "location": "test"
    }
    
    future = producer.send('iot-metrics', value=test_msg)
    producer.flush()
    
    print("   ✅ Kafka is accessible and accepting messages")
    producer.close()
    
except Exception as e:
    print(f"   ❌ Kafka connection failed: {e}")
    print("   → Make sure Kafka is running: docker compose up -d")

# Test 2: Check PySpark
print("\n2. Testing PySpark installation...")
try:
    from pyspark.sql import SparkSession
    
    spark = (
        SparkSession.builder
        .appName("Test")
        .config("spark.ui.enabled", "false")
        .getOrCreate()
    )
    
    # Quick DataFrame test
    data = [("device-1", 25.0), ("device-2", 26.5)]
    df = spark.createDataFrame(data, ["device_id", "temperature"])
    count = df.count()
    
    print(f"   ✅ PySpark is working (test DataFrame count: {count})")
    spark.stop()
    
except Exception as e:
    print(f"   ❌ PySpark test failed: {e}")
    print("   → Make sure Java is installed: java -version")

# Test 3: Check Flask
print("\n3. Testing Flask installation...")
try:
    from flask import Flask, jsonify
    
    app = Flask(__name__)
    
    @app.route('/test')
    def test():
        return jsonify({"status": "ok", "timestamp": datetime.now().isoformat()})
    
    print("   ✅ Flask is installed and importable")
    
except Exception as e:
    print(f"   ❌ Flask test failed: {e}")

# Test 4: Check project structure
print("\n4. Checking project structure...")
import os
from pathlib import Path

root = Path(__file__).parent
required_files = [
    "src/producer.py",
    "src/spark_streaming.py",
    "src/dashboard/app.py",
    "src/dashboard/templates/index.html",
    "docker-compose.yml",
    "requirements.txt",
    "README.md",
]

all_exist = True
for file in required_files:
    path = root / file
    if path.exists():
        print(f"   ✅ {file}")
    else:
        print(f"   ❌ {file} not found")
        all_exist = False

if all_exist:
    print("\n✅ All project files present")

# Test 5: Data directory
print("\n5. Checking data directory...")
data_dir = root / "data" / "aggregates"
data_dir.mkdir(parents=True, exist_ok=True)
print(f"   ✅ Data directory ready: {data_dir}")

print("\n" + "=" * 50)
print("Test complete! You're ready to run the pipeline.")
print("\nNext steps:")
print("  Terminal 1: python -m src.dashboard.app")
print("  Terminal 2: python -m src.spark_streaming")
print("  Terminal 3: python -m src.producer")
