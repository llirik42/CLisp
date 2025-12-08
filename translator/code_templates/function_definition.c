{{ ret_type }} {{ func }}({{ params | join(', ') }}) {
{% set tab = "\t" %}{% set newline = "\n" %}{% set lines = body.split("\n") if body != "" else [] %}{% for l in lines %}{{ tab }}{{ l }}
{% endfor %}{{ tab }}{% if ret_var %}return {{ ret_var }};{% else %}{% endif %}
}
