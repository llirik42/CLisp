{% set args_var = var+'_args' %}{{ type }} {{ args_var }}[] = {% raw %}{{% endraw %}{{ args | join(', ') }}{% raw %}}{% endraw %};
{{ type }} {{ var }} = {{ func }}({{ lambda_var }}, {{ args | length }}, {{ args_var }});
