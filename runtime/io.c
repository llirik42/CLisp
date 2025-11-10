#include "io.h"

#include <stdio.h>

#include "core.h"

Object* clisp_display(Object* obj) {
    // TODO:
    IntValue* v = obj->value;
    printf("%d\n", v->value);
    return NULL;
}