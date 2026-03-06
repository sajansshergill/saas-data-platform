create table if not exists analytics.dim_customer as
select
    customer_id,
    company_name,
    industry,
    signup_date,
    country,
    employee_count,
    status
from customers;

create table if not exists analytics.fact_revenue as
select
    payment_id,
    customer_id,
    subscription_id,
    payment_date,
    amount,
    payment_status
from payments;

create table if not exists analytics.fact_usage as
select
    event_id,
    customer_id,
    event_type, 
    event_timestamp,
    event_value
from usage_events;