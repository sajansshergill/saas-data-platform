select
    p.payment_id,
    p.customer_id,
    p.subscription_id,
    s.plan_name,
    p.payment_date,
    p.amount,
    p.payment_status
from {{ ref('stg_payments') }} p
left join {{ ref('stg_subscriptions') }} s
    on p.subscription_id = s.subscription_id
