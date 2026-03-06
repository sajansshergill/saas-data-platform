import pandas as pd
import random
from datetime import datetime, timedelta
from pathlib import Path

Path("data").mkdir(exist_ok=True)

records = []
event_types = ["login", "dashboard_view", "report_export", "api_call", "feature_use"]

for event_id in range(1, 2001):
    event_time = datetime.now() - timedelta(days=random.randint(0, 180), hours=random.randint(0, 23))
    records.append({
        "event_id": event_id,
        "customer_id": random.randint(1, 500),
        "event_type": random.choice(event_types),
        "event_timestamp": event_time,
        "event_value": random.randint(1, 20),
    })

df = pd.DataFrame(records)
df.to_csv("data/usage_events.csv", index=False)
print("Generated data/usage_events.csv")