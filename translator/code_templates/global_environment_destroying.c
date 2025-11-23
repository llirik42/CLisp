void {{ func }}({{ type }} {{ var }}) {
{% set tab = "\t" %}{% set lines = body.split("\n") if body != "" else [] %}{% for l in lines %}{{ tab }}{{ l }}{% endfor %}{{ tab }}
}
