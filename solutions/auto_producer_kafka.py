import time
import json
import random
from kafka import KafkaProducer
from kafka.errors import NoBrokersAvailable

BOOTSTRAP_SERVERS = "localhost:9092"
TOPIC = "test-payments"
RETRY_WAIT = 5
SEND_INTERVAL = 3

# wait for kafka to become healthy
print("Waiting for Kafka broker to become ready...")
while True:
    try:
        producer = KafkaProducer(                   # defines details about kafka client, including port, retries to connect, and timeout
            bootstrap_servers=BOOTSTRAP_SERVERS,
            value_serializer=lambda v: json.dumps(v).encode("utf-8"),
            retries=5,
            retry_backoff_ms=1000,
            request_timeout_ms=30000,
            api_version_auto_timeout_ms=30000
        )
        producer.partitions_for(TOPIC)              # if available, create partitions for test payments
        print("Kafka broker is ready!")
        break

    except NoBrokersAvailable:                      # if kafka is not available, retry every 5s
        print(f"Kafka not ready, retrying in {RETRY_WAIT}s...")
        time.sleep(RETRY_WAIT)

 

# send payment events 
payment_id = 1
print(f"Auto producer started. Sending payment every {SEND_INTERVAL} seconds...")       # send payment every 3s
try:
    while True:
        payment_event = {           # defines details about payment event, randomly generated 
            "id": payment_id,
            "amount": round(10 + 90 * (payment_id % 10) / 10, 2),
            "country_risk_score": round(random.uniform(0.1, 1.0), 2),
            "failed_logins": random.randint(0,6),
            "transaction_hour": random.randint(0,23),
            "is_new_device": random.choice([0, 1]),
            "currency": "USD",
            "status": "PENDING"
        }

        producer.send(TOPIC, payment_event)
        print(f"Sent payment event: {payment_event}")
        payment_id += 1
        time.sleep(SEND_INTERVAL)

except KeyboardInterrupt:           # keeps sending payments unless key is pressed, then producer closes 
    print("\nStopping producer...")

finally:
    producer.flush()
    producer.close()
print("Producer closed cleanly.")
