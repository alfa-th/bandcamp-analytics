{{ config(materialized="table") }}

with data as (
    select
        transaction_date, 

        sum(item_price_usd) as total_item_price,
        sum(amount_paid_usd) as total_amount_paid
    from {{ ref("fact") }}
    group by 1
)
select 
    *, 
    (data.total_amount_paid - data.total_item_price) as total_profit
from data