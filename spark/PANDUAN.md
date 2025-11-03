# Panduan Lengkap: Streaming IoT Metrics dengan Kafka → Spark → Dashboard

## 📋 Ringkasan Proyek

Proyek ini adalah contoh lengkap untuk belajar streaming data IoT menggunakan:
- **Kafka** sebagai message broker
- **PySpark Structured Streaming** untuk pemrosesan real-time
- **Flask** untuk dashboard visualisasi sederhana
- Semua menggunakan **native Python** (tanpa Scala/Java)

## 🏗️ Arsitektur

```
IoT Devices (Simulasi)
    ↓
[Kafka Producer] → publishes JSON metrics
    ↓
Kafka Topic: "iot-metrics"
    ↓
[PySpark Streaming] → reads, aggregates per window
    ↓
data/aggregates/latest.json (+ Parquet history)
    ↓
[Flask Dashboard] ← polls every 2s
    ↓
Web Browser (Chart.js)
```

## 📦 Struktur Folder

```
spark/
├── docker-compose.yml          # Kafka + Kafka UI
├── requirements.txt            # Python dependencies
├── README.md                   # English docs
├── PANDUAN.md                  # File ini
├── .gitignore
├── data/
│   └── .gitkeep               # Folder untuk output Spark
├── src/
│   ├── producer.py            # Kafka producer (simulator IoT)
│   ├── spark_streaming.py     # PySpark Structured Streaming
│   └── dashboard/
│       ├── __init__.py
│       ├── app.py             # Flask server
│       └── templates/
│           └── index.html     # Dashboard UI
```

## 🚀 Cara Menjalankan

### 1. Start Kafka dengan Docker

```zsh
docker compose up -d
```

Ini akan menjalankan:
- Kafka broker di `localhost:9092`
- Kafka UI di http://localhost:8080

### 2. Setup Python Environment

```zsh
# Buat virtual environment
python3 -m venv .venv

# Aktifkan venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

**Dependencies yang diinstall:**
- `pyspark==3.5.1` → Spark engine
- `kafka-python==2.0.2` → Kafka client
- `Flask==3.0.3` → Web framework

### 3. Jalankan 3 Proses (buka 3 terminal)

#### Terminal 1: Flask Dashboard
```zsh
source .venv/bin/activate
python -m src.dashboard.app
```
Buka browser ke: http://127.0.0.1:5000

#### Terminal 2: Spark Streaming Job
```zsh
source .venv/bin/activate
python -m src.spark_streaming
for mac : source .venv/bin/activate && export JAVA_HOME=$(/usr/libexec/java_home -v 17) && python -m src.spark_streaming
```
**Catatan:** First run akan download Kafka connector jars (~5-10 MB), tunggu sebentar.

#### Terminal 3: Kafka Producer (IoT Simulator)
```zsh
source .venv/bin/activate
python -m src.producer --devices 8 --rate 4.0
```

## 📊 Apa yang Terjadi?

### Producer (`src/producer.py`)
- Simulasi 8 devices IoT (bisa diubah dengan `--devices`)
- Setiap device publish metrics setiap ~250ms (4 msg/s dengan `--rate 4.0`)
- Format JSON:
  ```json
  {
    "device_id": "device-abc123",
    "ts": 1730638574123,
    "temperature": 24.7,
    "humidity": 55.3,
    "battery": 82.5,
    "status": "ok",
    "location": "lab"
  }
  ```

### Spark Streaming (`src/spark_streaming.py`)
- Membaca dari Kafka topic `iot-metrics`
- Parse JSON dan convert `ts` (epoch ms) ke timestamp
- Hitung agregat per **10 detik tumbling window**:
  - Count messages
  - Average temperature
  - Average humidity
  - Min/max battery
- Tulis hasil ke:
  - `data/aggregates/latest.json` → dashboard reads this
  - `data/aggregates/parquet/` → historical data

### Dashboard (`src/dashboard/app.py`)
- Flask server serve HTML di port 5000
- Endpoint `/metrics` return latest aggregates
- Frontend (Chart.js) polling setiap 2 detik
- Menampilkan:
  - Window range (10s)
  - Device count
  - Bar chart: Avg temperature per device
  - Bar chart: Avg humidity per device

## 🔧 Konfigurasi

### Kafka Topic & Bootstrap
Default: `localhost:9092` dan topic `iot-metrics`

Override dengan environment variables:
```zsh
export KAFKA_BOOTSTRAP="localhost:9092"
export KAFKA_TOPIC="iot-metrics"
python -m src.spark_streaming
```

### Window & Watermark
Edit `src/spark_streaming.py`:
```python
.groupBy(
    F.window(F.col("event_time"), "10 seconds"),  # ← window size
    ...
)
.withWatermark("event_time", "1 minute")  # ← late data tolerance
```

### Producer Rate
```zsh
# 10 devices, 2 messages/second per device
python -m src.producer --devices 10 --rate 2.0
```

## 🐛 Troubleshooting

### Error: "Cannot connect to Docker daemon"
```zsh
# Pastikan Docker Desktop running
open -a Docker

# Tunggu sampai Docker ready, lalu:
docker compose up -d
```

### Error: "Import pyspark could not be resolved"
Pastikan Java terinstall:
```zsh
java -version
# Jika belum ada:
brew install temurin
```

### Dashboard tidak ada data
Cek:
1. Producer running? (lihat logs di terminal)
2. Spark streaming running? (lihat logs, ada "Streaming started"?)
3. File exists? `ls -lh data/aggregates/latest.json`

### Spark download jars lambat
First run download `spark-sql-kafka-0-10` connector. Jika gagal, coba:
```zsh
# Pastikan internet stable
# Atau download manual dan set SPARK_HOME
```

## 📚 Konsep yang Dipelajari

1. **Kafka Basics**
   - Producer API
   - Topic & partitions
   - JSON serialization

2. **PySpark Structured Streaming**
   - `readStream` dari Kafka
   - JSON parsing dengan schema
   - Windowed aggregations
   - Watermarks untuk late data
   - `foreachBatch` sink

3. **Real-time Dashboard**
   - Polling-based updates
   - Chart.js visualizations
   - Flask REST API

4. **Docker Compose**
   - Single-broker Kafka (KRaft mode)
   - Container networking

## 🎯 Next Steps

- [ ] Tambah alerting: jika temperature > threshold
- [ ] Simpan ke database (PostgreSQL/MongoDB)
- [ ] Deploy ke cloud (AWS/GCP)
- [ ] Gunakan WebSocket untuk real-time push
- [ ] Tambah machine learning (anomaly detection)

## 🛑 Stop Everything

```zsh
# Stop Python processes: Ctrl+C di setiap terminal

# Stop Kafka:
docker compose down

# Hapus data volumes (optional):
docker compose down -v
```

## 📖 Referensi

- [PySpark Structured Streaming Guide](https://spark.apache.org/docs/latest/structured-streaming-programming-guide.html)
- [Kafka Python Client](https://kafka-python.readthedocs.io/)
- [Apache Kafka Docs](https://kafka.apache.org/documentation/)

---

**Selamat belajar streaming data! 🚀**
