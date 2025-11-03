import json
import os
import time
from pathlib import Path

from pyspark.sql import SparkSession, functions as F, types as T

DATA_DIR = Path(__file__).resolve().parent.parent / "data" / "aggregates"
LATEST_JSON = DATA_DIR / "latest.json"
PARQUET_DIR = DATA_DIR / "parquet"

KAFKA_BOOTSTRAP = os.environ.get("KAFKA_BOOTSTRAP", "localhost:9092")
KAFKA_TOPIC = os.environ.get("KAFKA_TOPIC", "iot-metrics")

# Match your installed PySpark version for the Kafka connector
SPARK_VERSION = "3.5.1"
KAFKA_PACKAGE = f"org.apache.spark:spark-sql-kafka-0-10_2.12:{SPARK_VERSION}"


def build_spark() -> SparkSession:
    spark = (
        SparkSession.builder.appName("IoT-Streaming-Kafka-Spark")
        .config("spark.sql.shuffle.partitions", "4")
        .config("spark.jars.packages", KAFKA_PACKAGE)
        .getOrCreate()
    )
    spark.sparkContext.setLogLevel("WARN")
    return spark


def ensure_dirs():
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    PARQUET_DIR.mkdir(parents=True, exist_ok=True)


def write_latest(batch_df, epoch_id: int):
    ensure_dirs()
    # Sort before writing (can't sort in streaming query, but OK here)
    sorted_df = batch_df.orderBy(F.col("window_start").desc(), F.col("device_id"))
    
    # Convert to JSON on driver (ok for small aggregated result sets)
    rows_json = sorted_df.toJSON().collect()
    payload = {
        "updated_at": int(time.time()),
        "records": [json.loads(r) for r in rows_json],
    }
    tmp_path = LATEST_JSON.with_suffix(".json.tmp")
    with open(tmp_path, "w", encoding="utf-8") as f:
        json.dump(payload, f)
    os.replace(tmp_path, LATEST_JSON)  # atomic

    # Optional: also persist historical aggregates to Parquet
    if sorted_df.count() > 0:
        (
            sorted_df
            .write
            .mode("append")
            .partitionBy("device_id")
            .parquet(str(PARQUET_DIR))
        )


def main():
    ensure_dirs()
    spark = build_spark()

    # Kafka source
    raw = (
        spark.readStream.format("kafka")
        .option("kafka.bootstrap.servers", KAFKA_BOOTSTRAP)
        .option("subscribe", KAFKA_TOPIC)
        .option("startingOffsets", "latest")
        .load()
    )

    # Parse JSON payload
    schema = T.StructType(
        [
            T.StructField("device_id", T.StringType()),
            T.StructField("ts", T.LongType()),  # epoch ms
            T.StructField("temperature", T.DoubleType()),
            T.StructField("humidity", T.DoubleType()),
            T.StructField("battery", T.DoubleType()),
            T.StructField("status", T.StringType()),
            T.StructField("location", T.StringType()),
        ]
    )

    parsed = (
        raw.select(F.col("key").cast("string").alias("key"), F.col("value").cast("string").alias("value"))
        .select(F.from_json(F.col("value"), schema).alias("data"))
        .select("data.*")
        .withColumn("event_time", F.from_unixtime((F.col("ts") / 1000)).cast(T.TimestampType()))
        .dropna(subset=["event_time", "device_id"])  # basic sanity
    )

    # Windowed aggregates per device
    windowed = (
        parsed
        .withWatermark("event_time", "1 minute")
        .groupBy(
            F.window(F.col("event_time"), "10 seconds").alias("window"),
            F.col("device_id"),
        )
        .agg(
            F.count("*").alias("count"),
            F.avg("temperature").alias("avg_temperature"),
            F.avg("humidity").alias("avg_humidity"),
            F.min("battery").alias("min_battery"),
            F.max("battery").alias("max_battery"),
        )
        .select(
            F.col("device_id"),
            F.col("window.start").alias("window_start"),
            F.col("window.end").alias("window_end"),
            "count",
            F.round("avg_temperature", 2).alias("avg_temperature"),
            F.round("avg_humidity", 2).alias("avg_humidity"),
            F.round("min_battery", 1).alias("min_battery"),
            F.round("max_battery", 1).alias("max_battery"),
        )
    )

    query = (
        windowed.writeStream.outputMode("update")
        .option("checkpointLocation", str(DATA_DIR / "_checkpoints"))
        .foreachBatch(write_latest)
        .trigger(processingTime="5 seconds")
        .start()
    )

    print("Streaming started. Writing latest aggregates to:", LATEST_JSON)
    print("Press Ctrl+C to stop.")

    try:
        query.awaitTermination()
    except KeyboardInterrupt:
        print("Stopping stream...")
    finally:
        query.stop()
        spark.stop()


if __name__ == "__main__":
    main()
