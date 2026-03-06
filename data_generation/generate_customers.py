from faker import Faker
import pandas as pd
import random
from pathlib import Path

fake = Faker()

Path("data").mkdir(exist_ok=True)

records = []
for customer in range(1, 501):
    records.append({
        "customer_id": customer,
        "company_name": fake.company(),
        "industry": random.choice(["Fintech", "Healthtech", "SaaS", "E-commerce", "EdTech"]),
        "signup_date": fake.date_between(start_date="-2y", end_date="today"),
        "country": fake.country(),
        "employee_count": random.choice([5, 10, 20, 50, 100, 250, 500]),
        "status": random.choice(["active", "active", "active", "inactive"])
    })
    
df = pd.DataFrame(records)
df.to_csv("data/customers.csv", index=False)
print("Generated data/customers.csv")