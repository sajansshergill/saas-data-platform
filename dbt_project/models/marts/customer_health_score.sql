with usage_summary as (
    select
        customer_id,
        count(*) as total_events,
        sum(Case when event_type = 'login' then 1 else 0 end) as logins,
        sum(Case when event_type = 'feature_use' then 1 else 0 end) as feature_uses
    from {{ ref('fact_usage') }}
    group by customer_id
),
payments_summary as (
    select
        customer_id,
        sum(case when payment_status = 'paid' then 1 else 0 end) as successful_payments,
        sum(case when payment_status = 'failed' then 1 else 0 end) as failed_payments
        sum(amount) as total_revenue
    from {{ ref('fact_revenue') }}
)
select
    c.customer_id,
    c.company_name,
    coalesce(u.total_events, 0) as total_events,
    coalesce(u.logins, 0) as logins,
    coalesce(u.feature_uses, 0) as feature_uses,
    coalesce(p.successful_payments, 0) as successful_payments,
    coalesce(p.failed_payments, 0) as failed_payments,
    coalesce(p.total_revenue, 0) as toal_revenue,
    (
        coalesce(u.total_events, 0) * 0.3 +
        coalesce(u.feature_uses, 0) * 0.3 +
        coalesce(p.successful_payments, 0) * 20 -
        coalesce(p.failed_payments, 0) * 10 
    ) as health_score
from {{ ref('dim_cutsomers') }} c
left join usage_summary u
    on c.customer_id = u.customer_id
left join payments_summary p
    on c.customer_id = p.customer_id