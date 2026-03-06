import subprocess

commands = [
    ["python", "data_generation/generate_customers.py"],
    ["python", "data_generation/generate_subscriptions.py"],
    ["python", "data_generation/generate_payments.py"],
    ["python", "data_generation/generate_usage_events.py"],
    ["python", "pipelines/ingest_csv_to_postgres.py"],
    ["python", "pipelines/postgres_to_warehouse.py"],
    ["python", "pipelines/data_quality_checks.py"],
]

for cmd in commands:
    print(f"Running: {' '.join(cmd)}")
    subprocess.run(cmd, check=True)
    
print("Pipeline completed successfully.")