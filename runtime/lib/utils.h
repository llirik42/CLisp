#pragma once
#include "core.h"

#define ERROR_BUF_SIZE 256

enum CountCheckingMode {
    EQUAL,
    GREATER,
};

void clisp_exit(char* message);

void clisp_exit_errno(char* message);

void check_func_arguments_count(const char* func_name, unsigned int args_count, unsigned int expected_count, enum CountCheckingMode mode);

void check_func_argument_type(const char* func_name, enum ObjectType type, enum ObjectType expected_type);

void check_func_argument_numeric_type(const char* func_name, enum ObjectType type);

double unwrap_numeric_to_double(Object* numeric);

unsigned char obj_to_boolean(Object* obj);

Object* unwrap_object(Object* obj);

void destroy_if_unwrapped(Object* origin, Object* unwrapped);

#define CHECK_FUNC_ARGUMENTS_COUNT(args_count, expected_count, mode) check_func_arguments_count(__func__, args_count, expected_count, mode)

#define CHECK_FUNC_ARGUMENT_TYPE(type, expected_type) check_func_argument_type(__func__, type, expected_type)

#define CHECK_FUNC_ARGUMENT_NUMERIC_TYPE(type) check_func_argument_numeric_type(__func__, type)
