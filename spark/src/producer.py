import argparse
import json
import random
import string
import time
from datetime import datetime, timezone

from kafka import KafkaProducer


def random_device_id(prefix: str = "device", length: int = 6) -> str:
    suffix = "".join(random.choices(string.ascii_lowercase + string.digits, k=length))
    return f"{prefix}-{suffix}"


def build_message(device_id: str) -> dict:
    now = datetime.now(timezone.utc)
    ts_ms = int(now.timestamp() * 1000)
    return {
        "device_id": device_id,
        "ts": ts_ms,  # epoch milliseconds
        "temperature": round(random.uniform(18.0, 35.0), 2),
        "humidity": round(random.uniform(30.0, 80.0), 2),
        "battery": round(random.uniform(10.0, 100.0), 1),
        "status": random.choice(["ok", "ok", "ok", "warn", "error"]),
        "location": random.choice(["floor-1", "floor-2", "lab", "office"]),
    }


def main():
    parser = argparse.ArgumentParser(description="IoT metrics Kafka producer")
    parser.add_argument("--bootstrap", default="localhost:9092", help="Kafka bootstrap servers")
    parser.add_argument("--topic", default="iot-metrics", help="Kafka topic name")
    parser.add_argument("--devices", type=int, default=8, help="Number of devices to simulate")
    parser.add_argument("--rate", type=float, default=4.0, help="Messages per second per device")
    parser.add_argument("--jitter", type=float, default=0.3, help="Random sleep jitter fraction (0..1)")
    args = parser.parse_args()

    producer = KafkaProducer(
        bootstrap_servers=args.bootstrap,
        value_serializer=lambda v: json.dumps(v).encode("utf-8"),
        key_serializer=lambda k: (k or "").encode("utf-8"),
        linger_ms=50,
        acks="all",
        retries=10,
        max_in_flight_requests_per_connection=5,
    )

    devices = [random_device_id() for _ in range(args.devices)]
    print(f"Producing to {args.topic} -> {args.bootstrap} for devices: {devices}")

    base_sleep = 1.0 / max(args.rate, 0.1)

    try:
        while True:
            for d in devices:
                msg = build_message(d)
                producer.send(args.topic, value=msg, key=d)
            # jittered sleep to avoid alignment
            sleep_time = base_sleep * random.uniform(1 - args.jitter, 1 + args.jitter)
            time.sleep(max(sleep_time, 0.01))
    except KeyboardInterrupt:
        print("\nStopping producer...")
    finally:
        producer.flush()
        producer.close()


if __name__ == "__main__":
    main()
