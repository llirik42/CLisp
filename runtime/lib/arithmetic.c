#include "arithmetic.h"

#include "const.h"
#include "utils.h"

Object* clisp_add(CLISP_FUNC_PARAMS) {

    CHECK_FUNC_ARGUMENTS_COUNT(count, 1, GREATER);

    int sum = 0;
    for (int i = 0; i < count; i++) {
        sum += get_int_value(args[i]);
    }

    return make_int(sum);
}
