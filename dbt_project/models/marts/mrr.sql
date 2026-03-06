select
    date_trunc('month', payment_date)::date AS revenue_month,
    sum(amount) as mrr
from {{ ref('fact_revenue') }}
where payment_status = 'paid'
group by 1
order by 1