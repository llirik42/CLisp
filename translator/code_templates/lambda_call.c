{% set _args = [args | length] + args %}
{{ type }} {{ var }} = {{ func }}({{ lambda_var }}, {{ _args | join(', ') }});
