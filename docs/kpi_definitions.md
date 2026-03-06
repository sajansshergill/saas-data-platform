# KPI Definitions

## Revenue Metrics

| KPI | Definition | Source |
|-----|------------|--------|
| **MRR** | Monthly Recurring Revenue – sum of paid amounts per month | `mrr.sql` |
| **ARR** | Annual Recurring Revenue – MRR × 12 | Derived |
| **ARPU** | Average Revenue Per User – total revenue / active paying customers per month | `arpu.sql` |
| **Revenue by Plan** | Total revenue and customer count by subscription plan | `revenue_by_plan.sql` |

## Customer Metrics

| KPI | Definition | Source |
|-----|------------|--------|
| **Churn Rate** | Cancelled customers / started customers per month | `churn_rate.sql` |
| **LTV** | Lifetime Value – total paid amount per customer | `ltv.sql` |
| **Customer Health Score** | Composite of usage events, logins, feature use, payments | `customer_health_score.sql` |

## Product Usage Metrics

| KPI | Definition | Source |
|-----|------------|--------|
| **Event Count** | Total usage events per customer | `fact_usage` |
| **Login Frequency** | Count of login events | `customer_health_score` |
| **Feature Adoption** | Count of feature_use events | `customer_health_score` |
