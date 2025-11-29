#include "runtime.h"

{% set tab = "\t" %}{% set newline = "\n" %}{% for f in declarations %}{{ f }}{{ newline }}{% endfor %}int main() {
{% set lines = main_body.split("\n") if main_body != "" else [] %}{% for l in lines %}{{ tab }}{{ l }}
{% endfor %}
{{ tab }}return 0;
}

