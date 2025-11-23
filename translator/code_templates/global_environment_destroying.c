void {{ func }}({{ type }} {{ var }}) {
{% set lines = body.split("\n") if body != "" else [] %}{% for l in lines %}{{ tab }}{{ l }}{% endfor %}{{ tab }}
}
