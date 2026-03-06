select
    customer_id,
    company_name,
    industry,
    signup_date,
    country,
    employee_count,
    status
from {{ ref('stg_customers') }}