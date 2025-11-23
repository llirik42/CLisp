{% set argList = var+'_args' %}{{ type }} {{ argList }}[] = {% raw %}{{% endraw %}{{ args | join(', ') }}{% raw %}}{% endraw %};
{{ type }} {{ var }} = {{ func }}({{ lambda_var }}, {{ args | length }}, {{ argList }});
