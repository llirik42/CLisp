#pragma once
#include "lib/environment.h"
#include "lib/core.h"

typedef CL_Object*(*cl_func_with_env)(CL_Environment* env, CL_FUNC_PARAMS);

typedef struct {
    enum CL_ObjectType type;
    unsigned short ref_count;
    union {
        cl_func cl_func;
        cl_func_with_env cl_func_with_env;
    } func;
    unsigned char with_env;
    CL_Environment* environment;
} CL_LambdaObject;

CL_Object* cl_make_lambda(cl_func_with_env func, CL_Environment* environment);

CL_Object* cl_make_lambda_without_env(cl_func func);

void cl_destroy_lambda(CL_Object* object);

CL_Object* cl_lambda_call(CL_Object* obj, CL_FUNC_PARAMS);
