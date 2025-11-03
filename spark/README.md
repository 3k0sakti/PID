# Streaming IoT Metrics: Kafka → Spark → Dashboard (Python)

An end-to-end, native Python example that streams simulated IoT metrics into Kafka, processes them with PySpark Structured Streaming, and visualizes live aggregates on a minimal Flask dashboard.

## What you get
- Kafka single-broker in Docker (KRaft mode, Apache Kafka 3.8.0)
- Python Kafka producer (`kafka-python`) generating IoT telemetry
- PySpark streaming job reading from Kafka and writing windowed aggregates
- Flask dashboard polling latest aggregates and rendering charts
- Kafka UI at http://localhost:8080

## Prereqs
- macOS with Docker Desktop running
- Python 3.10+ (with `pip`)
- Java 8+ installed (required by PySpark)

## Quick start

1) Start Kafka (Docker)

```zsh
docker compose up -d
# or: docker-compose up -d
```

2) Create & activate a virtualenv and install deps

```zsh
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

3) Run the Flask dashboard (Terminal A)

```zsh
python -m src.dashboard.app
# open http://127.0.0.1:5000
```

4) Start the Spark streaming job (Terminal B)

```zsh
python -m src.spark_streaming
```

The first run will download Spark Kafka connector jars; give it a minute.

5) Start the IoT producer (Terminal C)

```zsh
python -m src.producer --devices 8 --rate 4.0 --topic iot-metrics --bootstrap localhost:9092
```

You should see the dashboard update every ~2s with average temperature and humidity per device in the latest 10s window.

## How it works
- Producer publishes JSON such as:

```json
{
  "device_id": "device-2g7xqa",
  "ts": 1730638574123,
  "temperature": 24.7,
  "humidity": 55.3,
  "battery": 82.5,
  "status": "ok",
  "location": "lab"
}
```

- Spark reads from Kafka, parses JSON, converts `ts` (epoch ms) to `event_time`, then computes 10s tumbling window aggregates per device (avg temperature/humidity, battery min/max, count).
- Each micro-batch writes:
  - `data/aggregates/latest.json` (small payload the dashboard polls)
  - historical Parquet files in `data/aggregates/parquet/`

## Configs
- Kafka topic: `iot-metrics` (auto-created)
- Kafka bootstrap: `localhost:9092` (outside Docker) / `kafka:9092` (inside Docker)
- Window: 10 seconds, watermark: 1 minute

Env overrides:
- `KAFKA_BOOTSTRAP` and `KAFKA_TOPIC` for the Spark job
- `FLASK_HOST` and `FLASK_PORT` for the dashboard

## Troubleshooting
- Spark Kafka connector not found: ensure internet access; we set `spark.jars.packages` to `org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.1` matching PySpark 3.5.1
- PySpark requires Java. On macOS, install with e.g. `brew install temurin` then re-run.
- If no data on the dashboard, check:
  - Producer logs (messages being sent)
  - Spark logs (streaming started, no errors)
  - File `data/aggregates/latest.json` being updated

## Stop
```zsh
docker compose down
```
