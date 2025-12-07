{{ type }} {{ var }};
{{ pre_body }}
while (1) {
{% set tab = "\t" %}
{% set test_body_lines = test_body.split("\n") if test_body != "" else [] %}{% for l in test_body_lines %}{{ tab }}{{ l }}
{% endfor %}
{{ tab }}if ({{ test_value }}) {
{% set true_test_body_lines = true_test_body.split("\n") if true_test_body != "" else [] %}{% for l in true_test_body_lines %}{{ tab }}{{ tab }}{{ l }}
{% endfor %}
{{ tab }}{{ tab }}{{ var }} = {{ true_test_var }};
{{ tab }}{{ tab }}break;
{{ tab }}}
{% set false_test_body_lines = false_test_body.split("\n") if false_test_body != "" else [] %}{% for l in false_test_body_lines %}{{ tab }}{{ l }}
{% endfor %}
}
{{ post_body }}
