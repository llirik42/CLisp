{% set argList = var+'_args' %}Object* {{ argList }}[] = {% raw %}{{% endraw %}{{ test }}, {{ consequent }}, {{ alternate }}{% raw %}}{% endraw %};
Object* {{ var }} = clisp_if({{ argList }});
