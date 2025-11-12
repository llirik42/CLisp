#include "io.h"

#include <stdio.h>
#include <stdlib.h>

#include "core.h"

Object* clisp_display(unsigned int count, Object** args) {
    // TODO:
    if (count != 1) {
        fprintf(stderr, "display: exprected 1 argument!");
        exit(EXIT_FAILURE);
    }

    IntValue* v = args[0]->value;
    printf("%d\n", v->value);
    return NULL;
}
