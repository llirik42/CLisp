{{ type }} {{ var }};
{{ pre_body }}
{% set tab = "\t" %}if ({{ func }}({{ cond_var }})) {
{% set then_lines = then_body.split("\n") if then_body != "" else [] %}{% for l in then_lines %}{{ tab }}{{ l }}
{% endfor %}
{{ tab }}{{ var }} = {{ then_var }};
}
else {
{% set else_line = else_body.split("\n") if else_body != "" else [] %}{% for l in else_line %}{{ tab }}{{ l }}
{% endfor %}
{{ tab }}{{ var }} = {{ else_var }};
}
{{ post_body }}
