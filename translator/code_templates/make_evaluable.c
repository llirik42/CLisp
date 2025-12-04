{% set args_var = var+'_args' %}{{ type }} {{ args_var }}[] = {% raw %}{{% endraw %}{{ args | join(', ') }}{% raw %}}{% endraw %};
{{ type }} {{ var }} = {{ creation_func }}({{ func }}, {{ args | length }}, {{ args_var }});
