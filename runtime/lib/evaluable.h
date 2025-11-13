#pragma once
#include "core.h"

typedef struct {
    Object* (*function)(unsigned int, Object**);
    Object **args;
    unsigned int args_count;
} FunctionWrapper;

Object* make_evaluable(Object* (*func)(unsigned int, Object**), CLISP_FUNC_PARAMS);

void destroy_evaluable(Object* obj);

Object* evaluate(Object* function_wrapper_obj);
