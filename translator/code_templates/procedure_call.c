{% set args = [args | length] + args %}Object* {{ var }} = {{ function }}({{ args | join(', ') }});
