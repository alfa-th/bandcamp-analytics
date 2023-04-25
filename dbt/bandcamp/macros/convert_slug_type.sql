{#
    This macro returns the long description of slug type
#}

{% macro convert_slug_type(slug_type) %}
    case {{ slug_type }}
        when 'a' then 'Albums'
        when 't' then 'Merch'
        when 'p' then 'Tracks'
    end
{% endmacro %}