{{ type }} {{ func }}() {
{% set lines = body.split("\n") if body != "" else [] %}{% for l in lines %}{{ tab }}{{ l }}
{% endfor %}{{ tab }}return {{ var }};
}
