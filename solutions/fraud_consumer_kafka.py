import json
import joblib
from kafka import KafkaConsumer
import pandas as pd
import csv
import os
from datetime import datetime

# load .pkl model from train_fraud_model.py
model = joblib.load("fraud_model.pkl")

# define .csv log file
LOG_FILE = "fraud_scores_stream.csv"

# if file does not exist, create it with headers
if not os.path.exists(LOG_FILE):
    with open(LOG_FILE, mode="w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([
            "timestamp",
            "payment_id",
            "amount",
            "country_risk_score",
            "failed_logins",
            "transaction_hour",
            "is_new_device",
            "fraud_probability"
        ])

# connect to kafka consumer using "test-payments"
consumer = KafkaConsumer(
    "test-payments",
    # bootstrap_servers='host.docker.internal:9092',  # Docker-host Kafka
    bootstrap_servers="localhost:9092",
    auto_offset_reset="earliest",
    group_id="fraud_group"
)

print("Listening for payments...")


for message in consumer:
    try:
        payment_event = json.loads(message.value.decode("utf-8")) 
        print(f"Received payment: {payment_event}")     # confirmation that payment from producer is received 

        # build dataframe to get values from payment message
        X = pd.DataFrame([[
            payment_event.get("amount", 0),
            payment_event.get("country_risk_score", 0),
            payment_event.get("failed_logins", 0),
            payment_event.get("transaction_hour", 0),
            payment_event.get("is_new_device", 0)
        ]], columns=model.feature_names_in_)

        fraud_prob = model.predict_proba(X)[0][1]   # predicts fraud based on variables

        print(f"Fraud risk score = {fraud_prob:.2f}\n")

        # appends payment values to .csv, producing constant stream of events 
        with open(LOG_FILE, mode="a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([
                datetime.now().isoformat(),
                payment_event.get("payment_id", None),
                payment_event.get("amount"),
                payment_event.get("country_risk_score"),
                payment_event.get("failed_logins"),
                payment_event.get("transaction_hour"),
                payment_event.get("is_new_device"),
                round(float(fraud_prob), 4)
            ])

    except Exception as e:
        print(f"Error processing message: {e}")
