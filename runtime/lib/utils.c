#include "utils.h"

#include <assert.h>
#include <stdio.h>
#include <stdlib.h>

#include "objects/primitive.h"
#include "objects/evaluable.h"

void clisp_exit(char* message) {
    fprintf(stderr, "%s", message);
    abort();
}

void clisp_exit_errno(char* message) {
    perror(message);
    abort();
}

void check_func_arguments_count(const char* func_name, unsigned int args_count, unsigned int expected_count, enum CountCheckingMode mode) {
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
            clisp_exit("Unknown count checking mode.");
    }

    if (condition) {
        char error_str[ERROR_BUF_SIZE];
        snprintf(error_str, sizeof(error_str), format_str, func_name, expected_count, args_count);
        clisp_exit(error_str);
    }
}

void check_func_argument_type(const char* func_name, enum ObjectType type, enum ObjectType expected_type) {
    if (type != expected_type) {
        char error_str[ERROR_BUF_SIZE];
        snprintf(error_str, sizeof(error_str), "Wrong argument type in %s! Must be equal %s. Got %s.\n",
            func_name, get_object_type_name(expected_type), get_object_type_name(type));
        clisp_exit(error_str);
    }
}

void check_func_argument_numeric_type(const char* func_name, enum ObjectType type) {
    if (!is_numeric(type)) {
        char error_str[ERROR_BUF_SIZE];
        snprintf(error_str, sizeof(error_str), "Wrong argument type in %s! Must be numeric. Got %s.\n",
            func_name, get_object_type_name(type));
        clisp_exit(error_str);
    }
}

double unwrap_numeric_to_double(Object* numeric) {
    switch (get_object_type(numeric)) {
        case INTEGER: {
            return get_int_value(numeric);
        }
        case DOUBLE: {
            return get_double_value(numeric);
        }
        default:
            clisp_exit("Failed to unwrap numeric value. Invalid type.\n");
            __builtin_unreachable();
    }
}

unsigned char obj_to_boolean(Object* obj) {
    assert(get_object_type(obj) != EVALUABLE);

    if (get_object_type(obj) == BOOLEAN) {
        return get_boolean_value(obj);
    }

    return 1;
}

// Unwrap non-constant type. If evaluable - returns evaluated. If lambda - returns evaluated lambda.
Object* unwrap_object(Object* obj) {
    return evaluate(obj);
}

void destroy_if_unwrapped(Object* origin, Object* unwrapped) {
    if (get_object_type(origin) == EVALUABLE) {
        destroy_evaluable(unwrapped);
    }
}
