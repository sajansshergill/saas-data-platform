select
    cast(customer_id as int) as customer_id,
    trim(company_name) as company_name,
    trim(industry) as industry,
    cast(signup_date as date) as signup_date,
    trim(country) as country,
    cast(employee_count as integer) as employee_count,
    trim(status) as status
from {{ source('public', 'customers') }}