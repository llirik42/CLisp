#pragma once
#include "core.h"

typedef Object*(*postponed_func)(CLISP_FUNC_PARAMS);

typedef struct {
    enum ObjectType type;
    unsigned short ref_count;
    postponed_func function;
    Object **args;
    unsigned int args_count;
} EvaluableObject;

Object* clisp_make_evaluable(postponed_func func, CLISP_FUNC_PARAMS);

void destroy_evaluable(Object* obj);

Object* evaluate(Object* obj);
