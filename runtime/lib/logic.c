#include "logic.h"

#include "const.h"
#include "evaluable.h"
#include "utils.h"

Object* clisp_if(CLISP_FUNC_PARAMS) {
    CHECK_FUNC_ARGUMENTS_COUNT(count, 3, EQUAL);

    CHECK_FUNC_ARGUMENT_TYPE(get_object_type(args[0]), BOOLEAN);

    if (get_boolean_value(args[0])) {
        if (get_object_type(args[1]) == EVALUABLE) {
            return evaluate(args[1]);
        }
        return args[1];
    }

    if (get_object_type(args[2]) == EVALUABLE) {
        return evaluate(args[2]);
    }
    return args[2];
}

Object* clisp_greater(CLISP_FUNC_PARAMS) {
    CHECK_FUNC_ARGUMENTS_COUNT(count, 2, EQUAL);

    CHECK_FUNC_ARGUMENT_NUMERIC_TYPE(get_object_type(args[0]));
    CHECK_FUNC_ARGUMENT_NUMERIC_TYPE(get_object_type(args[1]));

    if (unwrap_numeric_to_double(args[0]) > unwrap_numeric_to_double(args[1])) {
        return make_true();
    }
    return make_false();
}
