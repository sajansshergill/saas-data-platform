from sqlalchemy import text

from db import get_engine

engine = get_engine()

sql_files = [
    "warehouse_sql/create_raw_tables.sql",
    "warehouse_sql/create_marts.sql",
]

with engine.begin() as conn:
    for file_path in sql_files:
        with open(file_path, "r") as f:
            sql = f.read()
            conn.execute(text(sql))
            print(f"Executed {file_path}")