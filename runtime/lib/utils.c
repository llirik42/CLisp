#include "utils.h"

#include <stdio.h>
#include <stdlib.h>

void print_error_and_exit(char* message, unsigned char use_perror) {
    if (!use_perror) {
        fprintf(stderr, "%s", message);
    } else {
        perror(message);
    }
    exit(EXIT_FAILURE);
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
            print_error_and_exit("Unknown count checking mode.", 0);
    }

    if (condition) {
        char error_str[256];
        snprintf(error_str, sizeof(error_str), format_str, func_name, expected_count, args_count);
        print_error_and_exit(error_str, 0);
    }
}

void check_func_argument_type(const char* func_name, enum ObjectType type, enum ObjectType expected_type) {
    if (type != expected_type) {
        char error_str[256];
        snprintf(error_str, sizeof(error_str), "Wrong argument type in %s! Must be equal %s. Got %s.\n",
            func_name, get_object_type_name(expected_type), get_object_type_name(type));
        print_error_and_exit(error_str, 0);
    }
}

void check_func_argument_numeric_type(const char* func_name, enum ObjectType type) {
    if (type != INTEGER && type != DOUBLE && type != RATIO) {
        char error_str[256];
        snprintf(error_str, sizeof(error_str), "Wrong argument type in %s! Must be numeric. Got %s.\n",
            func_name, get_object_type_name(type));
        print_error_and_exit(error_str, 0);
    }
}

double unwrap_numeric_to_double(Object* numeric) {
    switch (numeric->type) {
        case INTEGER: {
            IntValue* unwrapped_int = numeric->value;
            return unwrapped_int->value;
        }
        case DOUBLE: {
            DoubleValue* unwrapped_double = numeric->value;
            return unwrapped_double->value;
        }
        default:
            print_error_and_exit("Failed to unwrap numeric value. Invalid type.\n", 0);
            return 0.0;
    }
}
