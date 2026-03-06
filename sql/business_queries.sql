-- Monthly recurring revenue trend
select *
from mrr
order by revenue_month;

-- Average revenue per user by month
select *
from arpu
order by revenue_month;

-- Top customers by lifetime value
select *
from ltv
order by ltv desc
limit 20;

-- Revenue concentration by subscription plan
select *
from revenue_by_plan
order by total_revenue desc;

-- Highest risk customers based on health score
select
    customer_id,
    company_name,
    health_score
from customer_health_score
order by health_score asc
limit 20;
