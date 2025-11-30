{{ type }} {{ var }};
{{ test_pre }}
{% set tab = "\t" %}if ({{ func }}({{ test_var }})) {
{% set consequent_lines = consequent_body.split("\n") if consequent != "" else [] %}{% for l in consequent_lines %}{{ tab }}{{ l }}
{% endfor %}
{{ tab }}{{ var }} = {{ consequent_var }};
}
else {
{% set alternate_lines = alternate_body.split("\n") if alternate != "" else [] %}{% for l in alternate_lines %}{{ tab }}{{ l }}
{% endfor %}
{{ tab }}{{ var }} = {{ alternate_var }};
}
{{ test_after }}
