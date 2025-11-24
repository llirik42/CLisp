#pragma once
#include "lib/core.h"

typedef struct {
    enum ObjectType type;
    unsigned short ref_count;
    clisp_func function;
    Object **args;
    unsigned int args_count;
} EvaluableObject;

Object* clisp_make_evaluable(clisp_func func, CLISP_FUNC_PARAMS);

void destroy_evaluable(Object* obj);

Object* evaluate(Object* obj);
