#pragma once
#include "core.h"

enum CountCheckingMode {
    EQUAL,
    GREATER,
};

void print_error_and_exit(char* message, unsigned char use_perror);

void check_func_arguments_count(const char* func_name, unsigned int args_count, unsigned int expected_count, enum CountCheckingMode mode);

void check_func_argument_type(const char* func_name, enum ObjectType type, enum ObjectType expected_type);

void check_func_argument_numeric_type(const char* func_name, enum ObjectType type);

double unwrap_numeric_to_double(Object* numeric);

unsigned char obj_to_boolean(Object* obj);

void destroy_if_evaluable(Object* origin, Object* evaluated);

#define CHECK_FUNC_ARGUMENTS_COUNT(args_count, expected_count, mode) check_func_arguments_count(__func__, args_count, expected_count, mode)

#define CHECK_FUNC_ARGUMENT_TYPE(type, expected_type) check_func_argument_type(__func__, type, expected_type)

#define CHECK_FUNC_ARGUMENT_NUMERIC_TYPE(type) check_func_argument_numeric_type(__func__, type)
