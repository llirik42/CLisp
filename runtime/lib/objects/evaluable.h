#pragma once
#include "lib/core.h"

typedef struct {
    enum CL_ObjectType type;
    unsigned short ref_count;
    cl_func function;
    CL_Object **args;
    unsigned int args_count;
} CL_EvaluableObject;

CL_Object* cl_make_evaluable(cl_func func, CL_FUNC_PARAMS);

void cl_destroy_evaluable(CL_Object* obj);

CL_Object* cl_evaluate(CL_Object* obj);
