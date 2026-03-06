select
    plan_name,
    sum(amount) as total_revenue,
    count(distinct customer_id) as customers
from {{ ref('fact_revenue') }}
where payment_status = 'paid'
group by 1
order by total_revenue desc