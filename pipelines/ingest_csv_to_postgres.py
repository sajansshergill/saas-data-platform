import pandas as pd

from db import get_engine

engine = get_engine()

files = {
    "customers": "data/customers.csv",
    "subscriptions": "data/subscriptions.csv",
    "payments": "data/payments.csv",
    "usage_events": "data/usage_events.csv",
}

for table_name, path in files.items():
    df = pd.read_csv(path)
    df.to_sql(table_name, engine, if_exists="replace", index=False)
    print(f"Loaded {path} into table {table_name}")