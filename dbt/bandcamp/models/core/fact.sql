{{ config(materialized="table") }}

select
    _id,
    transaction_date,
    url,
    artist_name,
    album_title,
    item_type,
    slug_type,
    country,
    item_price,
    amount_paid,
    currency,
    item_price_usd,
    amount_paid_usd,
    (amount_paid_usd - item_price_usd) as amount_overpaid_usd,
    safe_divide(amount_paid_usd, item_price_usd) as paid_to_price_ratio
from {{ ref("stg_root") }}