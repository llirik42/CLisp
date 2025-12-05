{% set args_var = var+'_args' %}{{ arg_type }} {{ args_var }}[] = {% raw %}{{% endraw %}{{ args_types | join(', ') }}{% raw %}}{% endraw %};
{{ type }} {{ var }} = {{ calling_func }}({{ function }}, {{ library }}, {{result_type}}, {{ args_types | length }}, {{ args_var }});
