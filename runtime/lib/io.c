#include "io.h"

#include <stdio.h>
#include <stdlib.h>

#include "core.h"
#include "utils.h"

Object* clisp_display(unsigned int count, Object** args) {

    CHECK_FUNC_ARGUMENTS_COUNT(count, 1, EQUAL);

    IntValue* v = args[0]->value;
    printf("%d\n", v->value);
    return NULL;
}
