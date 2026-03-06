from datetime import datetime
from airflow import DAG
from airflow.operators.bash import BashOperator

default_args = {
    "owner": "sajan",
    "depends_on_past": False
}

with DAG(
    dag_id="saas_data_pipeline",
    default_args=default_args,
    start_date=datetime(2026, 1, 1),
    schedule="@daily",
    catchup=False
) as dag:

    generate_customers = BashOperator(
        task_id="generate_customers",
        bash_command="python data_generation/generate_customers.py"
    )

    generate_subscriptions = BashOperator(
        task_id="generate_subscriptions",
        bash_command="python data_generation/generate_subscriptions.py"
    )

    generate_payments = BashOperator(
        task_id="generate_payments",
        bash_command="python data_generation/generate_payments.py"
    )

    generate_usage_events = BashOperator(
        task_id="generate_usage_events",
        bash_command="python data_generation/generate_usage_events.py"
    )

    ingest_to_postgres = BashOperator(
        task_id="ingest_to_postgres",
        bash_command="python pipelines/ingest_csv_to_postgres.py"
    )

    build_warehouse = BashOperator(
        task_id="build_warehouse",
        bash_command="python pipelines/postgres_to_warehouse.py"
    )

    generate_customers >> generate_subscriptions >> generate_payments
    [generate_payments, generate_usage_events] >> ingest_to_postgres >> build_warehouse