import pandas as pd
import random
from datetime import datetime, timedelta
from pathlib import Path

Path("data").mkdir(exist_ok=True)

subscriptions = pd.read_csv("data/subscriptions.csv")
records = []
payment_id = 1

for _, row in subscriptions.iterrows():
    start_date = pd.to_datetime(row["start_date"])
    end_date = pd.to_datetime(row["cancel_date"]) if pd.notnull(row["cancel_date"]) else pd.Timestamp.today()

    payment_date = start_date
    while payment_date <= end_date:
        records.append({
            "payment_id": payment_id,
            "customer_id": row["customer_id"],
            "subscription_id": row["subscription_id"],
            "payment_date": payment_date.date(),
            "amount": row["monthly_amount"],
            "payment_status": random.choice(["paid", "paid", "paid", "failed"])
        })
        payment_id += 1
        payment_date += pd.DateOffset(months=1)

df = pd.DataFrame(records)
df.to_csv("data/payments.csv", index=False)
print("Generated data/payments.csv")