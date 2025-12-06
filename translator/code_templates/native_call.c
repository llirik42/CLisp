{% set _args_types = [args_types | length] + args_types %}
{{ type }} {{ var }} = {{ calling_func }}({{ function }}, {{ library }}, {{result_type}}, {{ _args_types | join(', ') }});
