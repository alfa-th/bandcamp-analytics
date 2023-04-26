{{ config(materialized="view") }}

select
    _id,
    utc_date as transaction_date,
    url,
    artist_name,
    album_title,
    {{ convert_item_type("item_type") }} as item_type,
    {{ convert_slug_type("slug_type") }} as slug_type,
    {{ filter_country("country") }} as country,
    item_price,
    amount_paid,
    currency,
    ((item_price / amount_paid) * amount_paid_usd) as item_price_usd,
    amount_paid_usd,
from {{ source("staging", "partitioned_clustered_root") }}