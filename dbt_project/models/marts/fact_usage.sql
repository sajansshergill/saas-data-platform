select
    event_id,
    customer_id,
    event_type,
    event_timestamp,
    event_value
from {{ ref('stg_usage_events') }}