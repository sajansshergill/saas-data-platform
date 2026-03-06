select
    cast(subscription_id as int) as subscription_id,
    cast(customer_id as integer) as customer_id,
    trim(plan_name) as plan_name,
    cast(monthly_amount as numeric) as monthly_amount,
    cast(start_date as date) as start_date,
    cast(cancel_date as date) as cancel_date,
    trim(status) as status
from {{ source('public', 'subscriptions') }}