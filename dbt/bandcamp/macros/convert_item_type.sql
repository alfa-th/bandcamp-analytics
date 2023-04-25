{#
    this macro returns the long description of item type
#}

{% macro convert_item_type(item_type) %}
    case {{ item_type }}
        when 'a' then 'digital album'
        when 't' then 'digital track'
        when 'p' then 'physical album'
    end
{% endmacro %}