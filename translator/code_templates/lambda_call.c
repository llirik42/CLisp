{% set _args = [args | length, scalar_args_count] + args %}
{{ type }} {{ var }} = {{ func }}({{ lambda_var }}, {{ _args | join(', ') }});
