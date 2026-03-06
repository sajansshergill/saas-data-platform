import pandas as pd
from sqlalchemy import inspect, text

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
    inspector = inspect(engine)
    if inspector.has_table(table_name):
        # Avoid DROP TABLE so dbt views depending on these tables don't break.
        with engine.begin() as conn:
            conn.execute(text(f"truncate table {table_name}"))
        df.to_sql(table_name, engine, if_exists="append", index=False)
    else:
        df.to_sql(table_name, engine, if_exists="replace", index=False)
    print(f"Loaded {path} into table {table_name}")