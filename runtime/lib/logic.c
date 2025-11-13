#include "logic.h"

#include <string.h>

#include "const.h"
#include "evaluable.h"
#include "utils.h"

Object* clisp_if(CLISP_FUNC_PARAMS) {
    // TODO: 2-3 ARGS
    CHECK_FUNC_ARGUMENTS_COUNT(count, 3, EQUAL);

    CHECK_FUNC_ARGUMENT_TYPE(get_object_type(args[0]), BOOLEAN);

    unsigned char test_value = get_boolean_value(args[0]);
    Object* consequent = args[1];
    Object* alternative = args[2];

    if (test_value) {
        return evaluate(consequent);
    }

    return evaluate(alternative);
}

Object* clisp_greater(CLISP_FUNC_PARAMS) {
    CHECK_FUNC_ARGUMENTS_COUNT(count, 2, EQUAL);

    Object* left_term = evaluate(args[0]);
    Object* right_term = evaluate(args[1]);

    CHECK_FUNC_ARGUMENT_NUMERIC_TYPE(get_object_type(left_term));
    CHECK_FUNC_ARGUMENT_NUMERIC_TYPE(get_object_type(right_term));

    if (unwrap_numeric_to_double(left_term) > unwrap_numeric_to_double(right_term)) {
        return make_true();
    }

    return make_false();
}

Object* clisp_not(CLISP_FUNC_PARAMS) {
    CHECK_FUNC_ARGUMENTS_COUNT(count, 1, EQUAL);

    Object* term = evaluate(args[0]);

    CHECK_FUNC_ARGUMENT_TYPE(get_object_type(term), BOOLEAN);

    if (get_boolean_value(term)) {
        return make_false();
    }
    return make_true();
}

Object* clisp_equal(CLISP_FUNC_PARAMS) {
    CHECK_FUNC_ARGUMENTS_COUNT(count, 2, EQUAL);

    Object* left_term = evaluate(args[0]);
    Object* right_term = evaluate(args[1]);

    if (get_object_type(left_term) != get_object_type(right_term)) {
        return make_false();
    }

    unsigned char result = 0;

    switch (get_object_type(left_term)) {
        case INTEGER:
            result = get_int_value(left_term) == get_int_value(right_term);
            break;
        case BOOLEAN:
            result = get_boolean_value(left_term) == get_boolean_value(right_term);
            break;
        case DOUBLE:
            result = get_double_value(left_term) == get_double_value(right_term);
            break;
        case STRING:
            result = strcmp(get_string_value(left_term), get_string_value(right_term));
            break;
        default:
            print_error_and_exit("Unexpected terminal type in clisp_equal", 0);
    }

    return make_boolean(result);
}
