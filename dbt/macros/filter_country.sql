{#
    This macro returns the long description of item type
#}

{% macro filter_country(country, filter_array) %}
    case 
        when country in ('C2', 'CW', 'HY', 'ME', 'XK')
            then "Unknown"
        else country
    end
{% endmacro %}