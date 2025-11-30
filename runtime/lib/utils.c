#include "utils.h"

#include <stdio.h>
#include <stdlib.h>

#include "objects/primitive.h"
#include "objects/evaluable.h"

void cl_abort(char* message) {
    fprintf(stderr, "%s", message);
    abort();
}

void cl_abort_errno(char* message) {
    perror(message);
    abort();
}

void cl_check_func_args_count(const char* func_name, unsigned int args_count, unsigned int expected_count, enum CL_CountCheckingMode mode) {
    const char* format_str = NULL;
    int condition = 0;

    switch (mode) {
        case EQUAL:
            format_str = "Count of arguments in %s must be equal %d! Got %d.\n";
            condition = args_count != expected_count;
            break;
        case GREATER:
            format_str = "Count of arguments in %s must be greater than %d! Got %d.\n";
            condition = args_count <= expected_count;
            break;
        default:
            cl_abort("Unknown count checking mode.");
    }

    if (condition) {
        char error_str[CL_ERROR_BUF_SIZE];
        snprintf(error_str, sizeof(error_str), format_str, func_name, expected_count, args_count);
        cl_abort(error_str);
    }
}

void cl_check_func_arg_type(const char* func_name, enum CL_ObjectType type, enum CL_ObjectType expected_type) {
    if (type != expected_type) {
        char error_str[CL_ERROR_BUF_SIZE];
        snprintf(error_str, sizeof(error_str), "Wrong argument type in %s! Must be equal %s. Got %s.\n",
            func_name, get_obj_type_name(expected_type), get_obj_type_name(type));
        cl_abort(error_str);
    }
}

void cl_check_func_arg_numeric_type(const char* func_name, enum CL_ObjectType type) {
    if (!cl_is_numeric(type)) {
        char error_str[CL_ERROR_BUF_SIZE];
        snprintf(error_str, sizeof(error_str), "Wrong argument type in %s! Must be numeric. Got %s.\n",
            func_name, get_obj_type_name(type));
        cl_abort(error_str);
    }
}

double cl_unwrap_numeric_to_double(CL_Object* numeric) {
    switch (cl_get_obj_type(numeric)) {
        case INTEGER: {
            return cl_get_int_value(numeric);
        }
        case DOUBLE: {
            return cl_get_double_value(numeric);
        }
        default:
            cl_abort("Failed to unwrap numeric value. Invalid type.\n");
            __builtin_unreachable();
    }
}

// Unwrap non-constant type. If evaluable - returns evaluated. If lambda - returns evaluated lambda.
CL_Object* cl_unwrap_obj(CL_Object* obj) {
    return cl_evaluate(obj);
}

void cl_destroy_if_unwrapped(CL_Object* origin, CL_Object* unwrapped) {
    if (cl_get_obj_type(origin) == EVALUABLE) {
        cl_destroy_evaluable(unwrapped);
    }
}
