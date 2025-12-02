#pragma once
#include "lib/core.h"
#include "lib/environment.h"

typedef CL_Object*(*cl_evaluable_func)(CL_Environment* env);

typedef struct {
    enum CL_ObjectType type;
    unsigned short ref_count;
    cl_evaluable_func function;
    CL_Environment* environment;
    CL_Object* result;
} CL_EvaluableObject;

CL_Object* cl_make_evaluable(cl_evaluable_func func, CL_Environment* env);

void cl_destroy_evaluable(CL_Object* obj);

CL_Object* cl_evaluate(CL_Object* obj);
