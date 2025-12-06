{% set func_args = [args | length, scalar_args_count] + args %}
{{ type }} {{ var }} = {{ func }}({{ lambda_var }}, {{ func_args | join(', ') }});
