import pandas as pd
import random
from datetime import datetime, timedelta
from pathlib import Path

Path("data").mkdir(exist_ok=True)

plans = {
    "Starter": 99,
    "Growth": 299,
    "Pro": 799,
    "Enterprise": 1999,
}

records = []
for subscription in range(1, 501):
    plan_name = random.choice(list(plans.keys()))
    start_date = datetime.today() - timedelta(days=random.randint(30, 700))
    status = random.choice(["active", "active", "active", "cancelled"])
    cancel_date = None
    if status == "cancelled":
        cancel_date = start_date + timedelta(days=random.randint(30, 300))

    records.append({
        "subscription_id": subscription,
        "customer_id": subscription,
        "plan_name": plan_name,
        "monthly_amount": plans[plan_name],
        "start_date": start_date.date(),
        "cancel_date": cancel_date.date() if cancel_date else None,
    })
    
df = pd.DataFrame(records)
df.to_csv("data/subscriptions.csv", index=False)
print("Generated data/subscriptions.csv")