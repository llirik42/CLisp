#pragma once
#include "core.h"

typedef struct {
    Object* (*function)(unsigned int, Object**);
    Object **args;
    unsigned int args_count;
} FunctionWrapper;

Object* make_evaluable(Object* (*func)(unsigned int, Object**), unsigned int count, Object** args);

Object* evaluate(Object* function_wrapper_obj);
