{% set argList = var+'_args' %}Object* {{ argList }}[] = {% raw %}{{% endraw %}{{ args | join(', ') }}{% raw %}}{% endraw %};
Object* {{ var }} = {{ function }}({{ argList }}, {{ args | length }});
