{{ args_type }} {{ args_var }}[] = {% raw %}{{% endraw %}{{ args | join(', ') }}{% raw %}}{% endraw %};
{% if var is defined %}{{ type }} {{ var }} = {% else %}{% endif %}{{ func }}({{ call_args | join(', ') }});
