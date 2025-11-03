# Penjelasan Lengkap IoT Streaming Pipeline

## 🎯 Tujuan Pembelajaran

Proyek ini mengajarkan konsep **streaming data pipeline** yang banyak digunakan di industri untuk:
- Real-time monitoring (IoT devices, aplikasi mobile, web analytics)
- Fraud detection di financial services
- Recommendation systems
- Log processing & observability

## 📊 Arsitektur Detail

```
┌─────────────────────────────────────────────────────────────────┐
│                     PRODUCER (IoT Simulator)                     │
│                         src/producer.py                          │
├─────────────────────────────────────────────────────────────────┤
│ • Simulasi 8 devices IoT                                        │
│ • Generate random metrics: temp, humidity, battery              │
│ • Publish ke Kafka topic "iot-metrics"                          │
│ • Rate: 4 messages/second per device = 32 msg/s total          │
└─────────────────────┬───────────────────────────────────────────┘
                      │ JSON over TCP
                      ▼
┌─────────────────────────────────────────────────────────────────┐
│                    KAFKA (Message Broker)                        │
│                    Docker: apache/kafka:3.8.0                    │
├─────────────────────────────────────────────────────────────────┤
│ Topic: iot-metrics                                              │
│ • Partitions: 3 (parallel processing)                           │
│ • Retention: default 7 days                                     │
│ • Port: 9092                                                    │
└─────────────────────┬───────────────────────────────────────────┘
                      │ Consumer reads stream
                      ▼
┌─────────────────────────────────────────────────────────────────┐
│              SPARK STREAMING (Processing Engine)                 │
│                    src/spark_streaming.py                        │
├─────────────────────────────────────────────────────────────────┤
│ 1. Read from Kafka (structured streaming)                       │
│ 2. Parse JSON payload                                           │
│ 3. Convert timestamp (epoch ms → TimestampType)                 │
│ 4. Apply watermark (1 min for late data)                        │
│ 5. Window aggregation (10 second tumbling)                      │
│    - Count messages                                             │
│    - AVG(temperature), AVG(humidity)                            │
│    - MIN(battery), MAX(battery)                                 │
│    GROUP BY device_id, window                                   │
│ 6. Write results every 5 seconds                                │
└─────────────────────┬───────────────────────────────────────────┘
                      │ Batch write (foreachBatch)
                      ▼
┌─────────────────────────────────────────────────────────────────┐
│                         DATA LAYER                               │
├─────────────────────────────────────────────────────────────────┤
│ 1. data/aggregates/latest.json (atomic write)                  │
│    └─> Dashboard reads this file                                │
│                                                                  │
│ 2. data/aggregates/parquet/ (historical)                        │
│    └─> Partitioned by device_id                                 │
│    └─> For later analytics / ML                                 │
│                                                                  │
│ 3. data/aggregates/_checkpoints/                                │
│    └─> Spark streaming state & offset tracking                  │
└─────────────────────┬───────────────────────────────────────────┘
                      │ HTTP polling (2s interval)
                      ▼
┌─────────────────────────────────────────────────────────────────┐
│                  DASHBOARD (Visualization)                       │
│                   src/dashboard/app.py                           │
├─────────────────────────────────────────────────────────────────┤
│ Flask server (port 5000)                                        │
│                                                                  │
│ Routes:                                                          │
│ • GET /         → serve HTML (Chart.js)                         │
│ • GET /metrics  → read latest.json, return as JSON             │
│                                                                  │
│ Frontend (index.html):                                          │
│ • Poll /metrics every 2 seconds                                 │
│ • Extract latest window data                                    │
│ • Render bar charts (temperature, humidity per device)         │
└─────────────────────────────────────────────────────────────────┘
                      │
                      ▼
              User's Web Browser
              http://127.0.0.1:5000
```

## 🔄 Data Flow Example

### 1. Producer generates message
```json
{
  "device_id": "device-abc123",
  "ts": 1730638574123,        // epoch milliseconds
  "temperature": 24.7,         // Celsius
  "humidity": 55.3,            // %
  "battery": 82.5,             // %
  "status": "ok",              // ok|warn|error
  "location": "lab"            // floor-1|floor-2|lab|office
}
```

### 2. Kafka stores in topic partition
- Key: `device-abc123` (ensures messages from same device go to same partition)
- Value: JSON string
- Offset: auto-incremented (e.g., 12345)

### 3. Spark reads & processes
```python
# Input: raw Kafka messages
# Parse JSON, extract fields
# Convert ts → event_time (timestamp)

# Window: 10 seconds
# Example: 14:30:00 - 14:30:10

# Aggregate per device in window:
{
  "device_id": "device-abc123",
  "window_start": "2024-11-03T14:30:00",
  "window_end": "2024-11-03T14:30:10",
  "count": 40,                      // 4 msg/s × 10s
  "avg_temperature": 24.52,
  "avg_humidity": 54.87,
  "min_battery": 80.1,
  "max_battery": 85.3
}
```

### 4. Write to latest.json
```json
{
  "updated_at": 1730638580,
  "records": [
    {
      "device_id": "device-abc123",
      "window_start": "2024-11-03T14:30:00",
      "window_end": "2024-11-03T14:30:10",
      "count": 40,
      "avg_temperature": 24.52,
      "avg_humidity": 54.87,
      "min_battery": 80.1,
      "max_battery": 85.3
    },
    // ... 7 more devices
  ]
}
```

### 5. Dashboard renders
- Polls `/metrics` → gets JSON above
- Extract latest window (newest `window_start`)
- Group by device
- Render 2 bar charts

## ⚙️ Konfigurasi Penting

### Spark Streaming Window
```python
# src/spark_streaming.py, line ~92
.groupBy(
    F.window(F.col("event_time"), "10 seconds"),  # Window size
    F.col("device_id"),
)
```

**Apa itu window?**
- Tumbling window: non-overlapping, fixed size
- Event time: berdasarkan timestamp data, bukan processing time
- 10 detik → setiap 10s, hitung agregat baru

**Mengapa tumbling?**
- Sederhana untuk dipelajari
- Cocok untuk dashboard yang update berkala
- Alternatif: sliding window (overlapping)

### Watermark
```python
# src/spark_streaming.py, line ~89
.withWatermark("event_time", "1 minute")
```

**Apa itu watermark?**
- Toleransi untuk late-arriving data
- Jika message datang > 1 menit late, discard
- Spark tidak tunggu selamanya untuk data terlambat

**Contoh:**
- Window: 14:30:00 - 14:30:10
- Watermark: 1 menit
- Spark akan finalize window setelah melihat data dengan timestamp 14:31:10

### Trigger Interval
```python
# src/spark_streaming.py, line ~124
.trigger(processingTime="5 seconds")
```

**Apa artinya?**
- Spark check Kafka setiap 5 detik
- Proses batch baru (micro-batch)
- Trade-off: lebih kecil = lebih real-time, tapi overhead lebih tinggi

## 🧪 Eksperimen untuk Belajar

### 1. Ubah window size
Ganti `"10 seconds"` → `"30 seconds"` di `spark_streaming.py`
**Efek:** Agregat per 30s, lebih smooth tapi kurang real-time

### 2. Tambah device count
```zsh
python -m src.producer --devices 20 --rate 10.0
```
**Efek:** 20 devices × 10 msg/s = 200 msg/s throughput

### 3. Tambah aggregation function
```python
# di spark_streaming.py, tambah:
F.stddev("temperature").alias("stddev_temp"),
```
**Efek:** Dashboard bisa show variability

### 4. Late data simulation
Edit `producer.py`, tambah random delay:
```python
import random
msg["ts"] = int((time.time() - random.uniform(0, 120)) * 1000)
```
**Efek:** Lihat watermark behavior (late data discarded)

## 📈 Metrics yang Bisa Dimonitor

### Kafka
- **Throughput:** messages/second
  ```zsh
  # Check via Kafka UI: http://localhost:8080
  ```

### Spark
- **Processing time:** berapa lama proses 1 batch?
- **Input rate:** records/second
- **Watermark:** current watermark value
  ```
  # Check di Spark logs (terminal 2)
  ```

### Dashboard
- **Latency:** dari message produced sampai tampil di chart
- **Update frequency:** seberapa sering data refresh?

## 🎓 Konsep Lanjutan

Setelah paham proyek ini, belajar:

1. **Exactly-once semantics**
   - Kafka transactions
   - Spark idempotent writes

2. **State management**
   - Session windows
   - Stream-stream joins

3. **Backpressure handling**
   - Kafka consumer lag
   - Spark adaptive batch sizing

4. **Monitoring & alerting**
   - Prometheus + Grafana
   - Dead letter queues

5. **Production deployment**
   - Kubernetes (Kafka, Spark on K8s)
   - Auto-scaling
   - High availability

## 🔗 Referensi Belajar

- [Kafka in Action (book)](https://www.manning.com/books/kafka-in-action)
- [Spark Structured Streaming Guide](https://spark.apache.org/docs/latest/structured-streaming-programming-guide.html)
- [Event Time vs Processing Time](https://www.oreilly.com/radar/the-world-beyond-batch-streaming-101/)

---

**Happy learning! Jika ada error, cek PANDUAN.md bagian Troubleshooting.** 🚀
