with subscription_base as (
    select
        date_trunc('month', start_date)::date as start_month,
        date_trunc('month', cancel_date)::date as cancel_month,
        customer_id,
        status
    from {{ ref('stg_subscriptions') }}
),
monthly_starts as (
    select
        start_month as metric_month,
        count(distinct customer_id) as started_customers
    from subscription_base
    where start_month is not null
    group by 1
),
monthly_churn as (
    select
        cancel_month as metric_month,
        count(distinct customer_id) as churned_customers
    from subscription_base
    where cancel_month is not null
    group by 1
)
select
    s.metric_month,
    s.started_customers,
    coalesce(c.churned_customers, 0) as churned_customers,
    case
        when s.started_customers = 0 then 0
        else round(coalesce(c.churned_customers, 0):: numeric / s.started_customers, 4)
    end as churn_rate
from monthly_starts s
left join monthly_churn c
    on s.metric_month = c.metric_month
order by 1