# Architecture

## Data Flow

```
Operational Systems
(Postgres / Stripe / Usage Events)
        │
        ▼
Data Ingestion Layer
(Python ETL Pipelines)
        │
        ▼
Raw Data Layer
(PostgreSQL public schema)
        │
        ▼
Transformation Layer
(dbt models / warehouse_sql)
        │
        ▼
Analytics Warehouse
(Fact + Dimension Tables)
        │
        ▼
BI Layer
(Metabase Dashboards)
```

## Components

| Component | Purpose |
|-----------|---------|
| `data_generation/` | Synthetic data for customers, subscriptions, payments, usage events |
| `pipelines/ingest_csv_to_postgres.py` | Loads CSV data into Postgres operational tables |
| `pipelines/postgres_to_warehouse.py` | Creates raw + analytics schemas, mart tables |
| `pipelines/data_quality_checks.py` | Validates null IDs, duplicates, negative amounts |
| `dbt_project/` | dbt staging and mart models for analytics |
| `dags/saas_data_pipeline.py` | Airflow DAG for orchestration |
| `scripts/run_all.py` | Single entry point for local runs |

## Schemas

- **public**: Operational tables (customers, subscriptions, payments, usage_events)
- **analytics**: Mart tables (dim_customer, fact_revenue, fact_usage) created by warehouse_sql
- **dbt**: dbt builds models in public (or configured schema) via staging and marts
