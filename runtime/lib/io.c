#include "io.h"

#include <stdio.h>

#include "const.h"
#include "core.h"
#include "evaluable.h"
#include "utils.h"

Object* clisp_display(CLISP_FUNC_PARAMS) {

    CHECK_FUNC_ARGUMENTS_COUNT(count, 1, EQUAL);

    printf("%d\n", get_int_value(evaluate(args[0])));
    return make_unspecified();
}
