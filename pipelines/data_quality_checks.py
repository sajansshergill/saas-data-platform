import pandas as pd

from db import get_engine

engine = get_engine()

checks = {
    "customers_null_ids": "select count(*) as cnt from customers where customer_id is null",
    "subscriptions_duplicate_ids": """
        select count(*) as cnt
        from (
            select subscription_id
            from subscriptions
            group by subscription_id
            having count(*) > 1
        ) t
    """,
    "payments_negative_amounts": "select count(*) as cnt from payments where amount < 0",
}

failed = False

for check_name, query in checks.items():
    result = pd.read_sql_query(query, engine)
    cnt = int(result.iloc[0]['cnt'])
    print(f"{check_name}: {cnt}")
    if cnt > 0:
        failed = True
        
if failed:
    raise ValueError("Data quality checks failed.")

print("All data quality checks passed.")