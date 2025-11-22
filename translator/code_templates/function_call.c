{% if var %}{{ type }} {{ var }} = {% else %}{% endif %}{{ func }}({{ args | join(', ') }});
