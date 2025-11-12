{% set argList = var+'_args' %}Object* {{ argList }}[] = {% raw %}{{% endraw %}{{ args | join(', ') }}{% raw %}}{% endraw %};
Object* {{ var }} = make_evaluable({{ function }}, {{ args | length }}, {{ argList }});
