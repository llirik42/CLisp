#include "comparation.h"

#include <math.h>
#include <string.h>

#include "utils.h"

#include "lib/objects/primitive.h"
#include "lib/exit/abort.h"

#define DOUBLE_EPSILON 1e-9

typedef bool (*comparison_fn)(double, double);

static bool greater_than(double a, double b) { return a > b; }
static bool greater_or_equal_than(double a, double b) { return a >= b; }
static bool less_than(double a, double b) { return a < b; }
static bool less_or_equal_than(double a, double b) { return a <= b; }

static CL_Object* numeric_comparison(CL_FUNC_PARAMS, const char* func_name, comparison_fn compare) {
    cl_check_func_args_count(func_name, count, 2, EQUAL);

    CL_Object* left_term = args[0];
    CL_Object* right_term = args[1];

    CL_CHECK_FUNC_ARG_NUMERIC_TYPE(cl_get_obj_type(left_term));
    CL_CHECK_FUNC_ARG_NUMERIC_TYPE(cl_get_obj_type(right_term));

    bool result = false;

    if (compare(cl_unwrap_numeric_to_double(left_term), cl_unwrap_numeric_to_double(right_term))) {
        result = true;
    }

    return cl_make_boolean(result);
}

CL_Object* cl_greater(CL_FUNC_PARAMS) {
    return numeric_comparison(CL_FUNC_PARAMS_WITHOUT_TYPES, __func__, greater_than);
}

CL_Object* cl_greater_or_equal(CL_FUNC_PARAMS) {
    return numeric_comparison(CL_FUNC_PARAMS_WITHOUT_TYPES, __func__, greater_or_equal_than);
}

CL_Object* cl_less(CL_FUNC_PARAMS) {
    return numeric_comparison(CL_FUNC_PARAMS_WITHOUT_TYPES, __func__, less_than);
}

CL_Object* cl_less_or_equal(CL_FUNC_PARAMS) {
    return numeric_comparison(CL_FUNC_PARAMS_WITHOUT_TYPES, __func__, less_or_equal_than);
}

CL_Object *cl_equal(CL_FUNC_PARAMS) {
    CL_CHECK_FUNC_ARGS_COUNT(count, 2, EQUAL);

    CL_Object* left_term = args[0];
    CL_Object* right_term = args[1];

    if (cl_is_numeric_internal(cl_get_obj_type(left_term)) && cl_is_numeric_internal(cl_get_obj_type(right_term))) {
        double left_double_value = cl_unwrap_numeric_to_double(left_term);
        double right_double_value = cl_unwrap_numeric_to_double(right_term);
        return cl_make_boolean(left_double_value == right_double_value);
    }

    if (cl_get_obj_type(left_term) != cl_get_obj_type(right_term)) {
        return cl_make_false();
    }

    bool result = false;

    switch (cl_get_obj_type(left_term)) {
        case INTEGER:
            result = cl_get_int_value(left_term) == cl_get_int_value(right_term);
            break;
        case BOOLEAN:
            result = cl_get_boolean_value(left_term) == cl_get_boolean_value(right_term);
            break;
        case DOUBLE:
            result = fabs(cl_get_double_value(left_term) - cl_get_double_value(right_term)) < DOUBLE_EPSILON;
            break;
        case CHAR:
            result = cl_get_char_value(left_term) == cl_get_char_value(right_term);
            break;
        case STRING:
            if (!strcmp(cl_get_string_value(left_term), cl_get_string_value(right_term))) {
                result = true;
            } else {
                result = false;
            }
            break;
        default:
            cl_abort("Unexpected terminal type in clisp_equal\n");
    }

    return cl_make_boolean(result);
}
