#include "runtime.h"

int main() {
{% set tab = "\t" %}{% set lines = code.split("\n") if code != "" else [] %}{% for l in lines %}{{ tab }}{{ l }}
{% endfor %}{{ tab }}return 0;
}
