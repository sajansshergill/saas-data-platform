select
    cast(payment_id as int) as payment_id,
    cast(customer_id as integer) as customer_id,
    cast(subscription_id as integer) as subscription_id,
    cast(payment_date as date) as payment_date,
    cast(amount as numeric) as amount,
    trim(payment_status) as payment_status
from {{ source('public', 'payments') }}