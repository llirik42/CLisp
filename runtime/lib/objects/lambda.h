#pragma once
#include "lib/environment.h"
#include "lib/core.h"

typedef Object*(*lambda)(Environment* env, CLISP_FUNC_PARAMS);

typedef struct {
    enum ObjectType type;
    unsigned short ref_count;
    lambda func;
    Environment* environment;
} LambdaObject;

Object* clisp_make_lambda(lambda func, Environment* environment);

void destroy_lambda(Object* object);

Object* clisp_lambda_call(Object* obj, CLISP_FUNC_PARAMS);
