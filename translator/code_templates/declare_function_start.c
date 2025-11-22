Object* {{ func }}(CLISP_FUNC_PARAMS, Environment* env) {
{% set tab = "\t" %}{% set lines = code.split("\n") if code != "" else [] %}{% for l in lines %}{{ tab }}{{ l }}
{% endfor %}{{ tab }}
