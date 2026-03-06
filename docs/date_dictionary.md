# Date Dictionary

| Field | Table | Type | Description |
|-------|-------|------|-------------|
| **signup_date** | customers | date | When the customer signed up |
| **start_date** | subscriptions | date | Subscription start date |
| **cancel_date** | subscriptions | date | Subscription cancellation date (null if active) |
| **payment_date** | payments | date | Date of payment |
| **event_timestamp** | usage_events | timestamp | When the usage event occurred |
| **revenue_month** | mrr, arpu | date | First day of month (date_trunc) for monthly aggregates |

## Conventions

- All dates stored as `DATE` or `TIMESTAMP` in Postgres
- Monthly aggregates use `date_trunc('month', col)::date`
- Null `cancel_date` indicates an active subscription
