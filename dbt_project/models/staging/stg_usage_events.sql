select
    cast(event_id as int) as event_id,
    cast(customer_id as integer) as customer_id,
    trim(event_type) as event_type,
    cast(event_timestamp as timestamp) as event_timestamp,
    cast(event_value as integer) as event_value
from {{ source('public', 'usage_events') }}