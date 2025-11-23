{% set argList = var+'_args' %}{{ type }} {{ argList }}[] = {% raw %}{{% endraw %}{{ args | join(', ') }}{% raw %}}{% endraw %};
{{ type }} {{ var }} = {{ creation_func }}({{ func }}, {{ args | length }}, {{ argList }});
