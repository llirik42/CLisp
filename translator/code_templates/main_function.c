#include "runtime.h"

int main() {
{% set tab = "\t" %}{% set lines = code.split("\n") %}{% for l in lines %}{{ tab }}{{ l }}
{% endfor %}{{ tab }}return 0;
}
