with revenue_per_customer as (
    select 
        customer_id,
        sum(amount) as lifetime_revenue
    from {{ ref('fact_revenue') }}
    where payment_status = 'paid'
    group by 1
)
select
    customer_id,
    lifetime_revenue as ltv
from revenue_per_customer
order by ltv desc