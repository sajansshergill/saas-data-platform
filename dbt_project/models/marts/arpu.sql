with monthly_revenue as (
    select
        date_trunc('month', payment_date)::date as revenue_month,
        sum(amount) as total_revenue
    from {{ ref('fact_revenue') }}
    where payment_status = 'paid'
    group by 1
),
monthly_customers as (
    select
        date_trunc('month', payment_date)::date as revenue_month,
        count(distinct customer_id) as active_customers
    from {{ ref('fact_revenue') }}
    where payment_status = 'paid'
    group by 1
)
select
    r.revenue_month,
    r.total_revenue,
    c.active_customers,
    case
        when c.active_customers = 0 then 0
        else r.total_revenue / c.active_customers
    end as arpu
from monthly_revenue r
left join monthly_customers c
    on r.revenue_month = c.revenue_month
order by 1