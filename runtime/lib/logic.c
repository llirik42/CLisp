#include "logic.h"

#include "const.h"
#include "evaluable.h"
#include "utils.h"

Object* clisp_if(unsigned int count, Object** args) {
    CHECK_FUNC_ARGUMENTS_COUNT(count, 3, EQUAL);

    CHECK_FUNC_ARGUMENT_TYPE(args[0]->type, BOOLEAN);

    BooleanValue* test = args[0]->value;

    if (test->value) {
        if (args[1]->type == EVALUABLE) {
            return evaluate(args[1]);
        }
        return args[1];
    }

    if (args[2]->type == EVALUABLE) {
        return evaluate(args[2]);
    }
    return args[2];
}

Object* clisp_greater(unsigned int count, Object** args) {
    CHECK_FUNC_ARGUMENTS_COUNT(count, 2, EQUAL);

    CHECK_FUNC_ARGUMENT_NUMERIC_TYPE(args[0]->type);
    CHECK_FUNC_ARGUMENT_NUMERIC_TYPE(args[1]->type);

    if (unwrap_numeric_to_double(args[0]) > unwrap_numeric_to_double(args[1])) {
        return make_boolean(1);
    }
    return make_boolean(0);
}
