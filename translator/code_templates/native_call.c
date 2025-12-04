{% set args_formatted = [] %}{% for a, b in args %}{% set _ = args_formatted.append('{' ~ a ~ ', ' ~ b ~ '}') %}{% endfor %}{% set args_var = var+'_args' %}{{ arg_type }} {{ args_var }}[] = {% raw %}{{% endraw %}{{ args_formatted | join(', ') }}{% raw %}}{% endraw %};
{{ type }} {{ var }} = {{ calling_func }}({{ func }}, {{ library }}, {{result_type}}, {{ args | length }}, {{ args_var }});
