# SaaS Revenue & Customer Intelligence Data Platform
End-to-end analytics platform that simulates first Data Engineer building the data infrastructure for a B2B Saas startup.

The platform ingests operational data from application databases, payment systems, and product usage events and transforms into **reliable business metrics such as MRR, churn rate, ARPU, LTV and customer health scores,**

This project demonstrates how a startup can build a **scalable analytics stack from scratch** to support leadership KPIs, data analysts, and BI dashboards.

## Architecture Overview
Operational Systems
(Postgres / Stripe / Usage Events)
        │
        ▼
Data Ingestion Layer
(Python ETL Pipelines)
        │
        ▼
Raw Data Layer
(BigQuery / Snowflake)
        │
        ▼
Transformation Layer
(dbt models)
        │
        ▼
Analytics Warehouse
(Fact + Dimension Tables)
        │
        ▼
BI Layer
(Metabase Dashboards)

## Project Goals
The goal of this project is to simulate the responsibilities of the first data Engineer at a startup, including:
- Building the foundational **data warehouse**
- Creating **data ingestion pipelines**
- Designing **analytics data models**
- Implementing **data quality checks**
- Enabling **self-serve business intelligence**
- Defining a **single source of truth for KPIs**

## Tech Stack
| Layer            | Tools                |
| ---------------- | -------------------- |
| Programming      | Python               |
| Data Warehouse   | BigQuery / Snowflake |
| Transformation   | dbt                  |
| Orchestration    | Airflow              |
| Data Generation  | Faker                |
| Containerization | Docker               |
| BI / Dashboards  | Metabase             |
| Query Language   | SQL                  |

## Data Sources:
The platform simulates typical B2B SaaS operational systems.

### Application Database
(PostgreSQL)

Tables:
users
accounts
subscriptions
product_plans

### Payment System (Stripe-like)
invoices
payments
refunds

### Product Usage Events
usage_events
feature_usage
api_requests
logins

### CRM Data
leads
accounts
opportunities

Synthetic datasets are generated using Python + Faker to simulate real Saas business activity.

## Data Warehouse Architecture
The warehouse follows a **modern analytics stack layered architecture.**

### Raw Layer
Contains ingested source data
raw_customers
raw_subscriptions
raw_payments
raw_usage_events
raw_invoices

### Staging Layer
Standardized cleaned datasets.
stg_customers
stg_subscriptions
stg_payments
stg_usage_events

Transformations include:
- column normalization
- timestamp standardization
- deduplication
- type casting

### Analytics Layer
Dimensional models optimized for analytics

#### Dimension Tables
dim_customer
dim_product
dim_subscription_plan
dim_date

#### Fact Tables
fact_revenue
fact_usage
fact_payments
fact_subscriptions

## Business Metrics
The platform produces key SaaS KPIs used by leadership teams.

### Revenue Metrics
Monthly Recurring Revenue (MRR)
Annual Recurring Revenue (ARR)
Average Revenue Per User (ARPU)
Revenue Growth Rate

### Customer Metrics
Customer Churn Rate
Customer Lifetime Value (LTV)
Customer Health Score
Active Customers

### Product Usage Metrics
Daily Active Users
Feature Adoption
API Request Volume
Session Frequency

## Data Pipelines
Pipelines orchestrated using **Airflow DAGs.**

Example workflow:
extract_app_database
extract_stripe_payments
extract_usage_events
load_raw_tables
run_dbt_transformations
execute_data_quality_checks
publish_metrics_tables
refresh_bi_dashboards

Pipeline schedule:
Daily ingestion
Hourly usage ingestion
Nightly analytics models

## Data Quality & Observability
Data quality checks ensure reliable metrics.

### dbt Tests
not_null(customer_id)
unique(subscription_id)
accepted_values(subscription_status)
payment_amount > 0

### Freshness Monitoring
Checks that source tables are updated regularly.
Example:
usage_events updated within last 1 hour
payments updated within last 24 hours

## BI Dashboards
The warehouse powers **self-serve dashboards for business teams.**

### Executive Revenue Dashboard
Tracks:
- Monthly Recurring Revenue
- Churn Rate
- Revenue Growth
- Net Revenue Retention

### Customer Health Dashboard
Tracks:
- product usage
- payment activity
- churn risk
- customer engagements

## Repository Structure
<img width="225" height="628" alt="image" src="https://github.com/user-attachments/assets/43781700-41f5-4a76-998d-62b16c52758d" />

## How to Run the Project

### Quick start (all-in-one)

```bash
# 1. Clone and setup
git clone https://github.com/username/saas-data-platform
cd saas-data-platform

# 2. Install deps and env
pip install -r requirements.txt
cp .env.example .env

# 3. Database (choose one)
# Option A: Docker Postgres
docker-compose up -d

# Option B: Local Postgres (create DB, omit POSTGRES_USER in .env for Mac)
createdb saas_platform

# 4. Run full pipeline
python scripts/run_all.py
```

### What `run_all.py` does

1. Generates synthetic data (customers, subscriptions, payments, usage_events)
2. Ingests CSVs into Postgres
3. Builds warehouse tables (raw + analytics)
4. Runs data quality checks

### Optional: dbt models

```bash
# Copy profiles for dbt (or set DBT_PROFILES_DIR=.)
cp profiles.yml ~/.dbt/profiles.yml

# Run dbt
cd dbt_project && dbt run && dbt test
```

### Optional: Airflow / Metabase

Start `docker-compose up` for Airflow and Metabase, then trigger the `saas_data_pipeline` DAG.

## Example Business Insight
Using the analytics models, leadership teams can answer questions such as:
- Which customer segments generate the most revenue?
- What features drive customer retention?
- Which accounts show early churn risk signals?
- How is monthly recurring revenue trending?

## Dashboard Preview

### Executive Revenue Dashboard
Tracks monthly recurring revenue, ARPU, churn, and revenue by plan.

![Executive Revenue Dashboard](docs/images/revenue_dashboard.png)

### Customer Health Dashboard
Tracks usage intensity, payment reliability, and customer health score.

![Customer Health Dashboard](docs/images/customer_health_dashboard.png)

### Pipeline Orchestration
Airflow DAG for synthetic generation, ingestion, warehouse builds, and validation.

![Airflow DAG](docs/images/airflow_dag.png)