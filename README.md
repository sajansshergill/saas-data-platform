# SaaS Revenue & Customer Intelligence Data Platform
End-to-end analytics platform that simulates first Data Engineer building the data infrastructure for a B2B Saas startup.

The platform ingests operational data from application databases, payment systems, and product usage events and transforms into **reliable business metrics such as MRR, churn rate, ARPU, LTV and customer health scores,**

This project demosntrates how a stratup can build a **scalable analytics stack from scratch** to support leadership KPIs, data analysts, and BI dashboards.

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
(db t models)
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
- Desigining **analytics data models**
- Implementing **data quality checks**
- Enabling **self-serve business intelligence**
- Defining a **single source of truth for KPIS**

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

## Data Soucres:
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
opportiunities

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

## Business Maetrics
The platform produces key SaaS KPIs used by leadership teams.

### Revenue Metrics
Monthly Recurring Revenue (MRR)
Annual Recurring Revenue (ARR)
Average Revenue Per User (ARPU)
Revenue Growth Rate

### Customer Metrics
Customer Churn Rate
Customer Lifetime Value (LTV)
Customer Health Source
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

## Data Quallity & Observability
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
payments updatd with last 24 hours

## BI Dashboards
The warehourse powers **self-serve dashboards for business teams.**

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
1. Clone the Repository
git clone https://github.com/username/saas-data-platform
cd saas-data-platform

2. Start Infrastructure
docker-compose up
This launches:
- Airflow
- Postgres
- dbt environment
- Metabase

3. Generate Synthetic Data
python data_generation/generate_customers.py
python data_generation/generate_usage_events.py

4. Run Pipelines
Trigger the Airflow DAG:
saas_data_pipeline

5. Run Transformations
dbt run
dbt test

6. Explore Dashboards
Open:
http://localhost:3000
View business dashboards in **Metabase**.

## Example Business Insight
Using the analytics models, leadership teams can answer questions such as:
- Which customer segments generate the most revenue?
- What features drive customer retention?
- Which accounts show early churn risk signals?
- How is monthly recurring revenue trending?
