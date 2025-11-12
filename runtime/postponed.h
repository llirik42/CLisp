#pragma once
#include "core.h"

typedef struct {
    Object* (*function)(int, Object**);
    Object **args;
    int args_count;
} FunctionWrapper;

Object* make_evaluable(Object* (*func)(int, Object**), int count, Object** args);

Object* evaluate(const Object* function_wrapper_obj);
