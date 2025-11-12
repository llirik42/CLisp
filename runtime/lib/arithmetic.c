#include "arithmetic.h"

#include "const.h"
#include "utils.h"

Object* clisp_add(unsigned int count, Object** args) {

    CHECK_FUNC_ARGUMENTS_COUNT(count, 1, GREATER);

    int sum = 0;
    for (int i = 0; i < count; i++) {
        IntValue* v1 = args[i]->value;
        sum += v1->value;
    }

    return make_int(sum);
}
