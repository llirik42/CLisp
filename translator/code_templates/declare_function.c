{{ ret_type }} {{ func }}({{ params | join(', ') }}) {
{% set tab = "\t" %}{% set newline = "\n" %}{% set lines = code.split("\n") if code != "" else [] %}{% for l in lines %}{{ tab }}{{ l }}
{% endfor %}{% if ret %}{{ tab }}return {{ ret }};
{% else %}{% endif %}}
