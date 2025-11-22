#include "runtime.h"

{% set newline = "\n" %}{% for f in declarations %}{{ f }}{{ newline }}{% endfor %}int main() {
{% set tab = "\t" %}{% set lines = main_body.split("\n") if main_body != "" else [] %}{% for l in lines %}{{ tab }}{{ l }}
{% endfor %}{{ tab }}return 0;
}
