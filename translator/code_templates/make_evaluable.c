{% set args = [args | length] + args %}Object* {{ var }} = make_evaluable({{ function }}, {{ args | join(', ') }});
