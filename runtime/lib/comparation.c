#include "comparation.h"

#include <string.h>

#include "primitive.h"
#include "utils.h"

typedef unsigned int (*comparison_fn)(double, double);

static unsigned int greater_than(double a, double b) { return a > b; }
static unsigned int greater_or_equal_than(double a, double b) { return a >= b; }
static unsigned int less_than(double a, double b) { return a < b; }
static unsigned int less_or_equal_than(double a, double b) { return a <= b; }

static Object* numeric_comparison(CLISP_FUNC_PARAMS, const char* func_name, comparison_fn compare) {
    check_func_arguments_count(func_name, count, 2, EQUAL);

    Object* left_term = unwrap_object(args[0]);
    Object* right_term = unwrap_object(args[1]);

    CHECK_FUNC_ARGUMENT_NUMERIC_TYPE(get_object_type(left_term));
    CHECK_FUNC_ARGUMENT_NUMERIC_TYPE(get_object_type(right_term));

    unsigned char result = 0;

    if (compare(unwrap_numeric_to_double(left_term), unwrap_numeric_to_double(right_term))) {
        result = 1;
    }
    destroy_if_unwrapped(args[0], left_term);
    destroy_if_unwrapped(args[1], right_term);

    return make_boolean(result);
}

Object* clisp_greater(CLISP_FUNC_PARAMS) {
    return numeric_comparison(CLISP_FUNC_PARAMS_WITHOUT_TYPES, __func__, greater_than);
}

Object* clisp_greater_or_equal(CLISP_FUNC_PARAMS) {
    return numeric_comparison(CLISP_FUNC_PARAMS_WITHOUT_TYPES, __func__, greater_or_equal_than);
}

Object* clisp_less(CLISP_FUNC_PARAMS) {
    return numeric_comparison(CLISP_FUNC_PARAMS_WITHOUT_TYPES, __func__, less_than);
}

Object* clisp_less_or_equal(CLISP_FUNC_PARAMS) {
    return numeric_comparison(CLISP_FUNC_PARAMS_WITHOUT_TYPES, __func__, less_or_equal_than);
}

Object *clisp_equal(CLISP_FUNC_PARAMS) {
    CHECK_FUNC_ARGUMENTS_COUNT(count, 2, EQUAL);

    Object* left_term = unwrap_object(args[0]);
    Object* right_term = unwrap_object(args[1]);

    if (is_numeric(get_object_type(left_term)) && is_numeric(get_object_type(right_term))) {
        double left_double_value = unwrap_numeric_to_double(left_term);
        double right_double_value = unwrap_numeric_to_double(right_term);
        destroy_if_unwrapped(args[0], left_term);
        destroy_if_unwrapped(args[1], right_term);
        return make_boolean(left_double_value == right_double_value);
    }

    if (get_object_type(left_term) != get_object_type(right_term)) {
        destroy_if_unwrapped(args[0], left_term);
        destroy_if_unwrapped(args[1], right_term);
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
        case CHAR:
            result = get_char_value(left_term) == get_char_value(right_term);
            break;
        case STRING:
            if (!strcmp(get_string_value(left_term), get_string_value(right_term))) {
                result = 1;
            } else {
                result = 0;
            }
            break;
        default:
            print_error_and_exit("Unexpected terminal type in clisp_equal\n", 0);
    }

    destroy_if_unwrapped(args[0], left_term);
    destroy_if_unwrapped(args[1], right_term);

    return make_boolean(result);
}
