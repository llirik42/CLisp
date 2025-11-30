#pragma once
#include "core.h"

#define CL_ERROR_BUF_SIZE 256

enum CountCheckingMode {
    EQUAL,
    GREATER,
};

void cl_abort(char* message);

void cl_abort_errno(char* message);

void cl_check_func_args_count(const char* func_name, unsigned int args_count, unsigned int expected_count, enum CountCheckingMode mode);

void cl_check_func_arg_type(const char* func_name, enum CL_ObjectType type, enum CL_ObjectType expected_type);

void cl_check_func_arg_numeric_type(const char* func_name, enum CL_ObjectType type);

double cl_unwrap_numeric_to_double(CL_Object* numeric);

unsigned char cl_obj_to_boolean(CL_Object* obj);

CL_Object* cl_unwrap_obj(CL_Object* obj);

void cl_destroy_if_unwrapped(CL_Object* origin, CL_Object* unwrapped);

#define CL_CHECK_FUNC_ARGS_COUNT(args_count, expected_count, mode) cl_check_func_args_count(__func__, args_count, expected_count, mode)

#define CL_CHECK_FUNC_ARG_TYPE(type, expected_type) cl_check_func_arg_type(__func__, type, expected_type)

#define CL_CHECK_FUNC_ARG_NUMERIC_TYPE(type) cl_check_func_arg_numeric_type(__func__, type)
