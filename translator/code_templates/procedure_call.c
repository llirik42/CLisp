{% set argList = var+'_args' %}{{ type }} {{ argList }}[] = {% raw %}{{% endraw %}{{ args | join(', ') }}{% raw %}}{% endraw %};
{{ type }} {{ var }} = {{ func }}({{ args | length }}, {{ argList }});
