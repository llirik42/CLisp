#pragma once
#include "lib/environment.h"
#include "lib/core.h"

typedef Object*(*clisp_func_with_env)(Environment* env, CLISP_FUNC_PARAMS);

typedef struct {
    enum ObjectType type;
    unsigned short ref_count;
    union {
        clisp_func clisp_func;
        clisp_func_with_env clisp_func_with_env;
    } func;
    unsigned char with_env;
    Environment* environment;
} LambdaObject;

Object* clisp_make_lambda(clisp_func_with_env func, Environment* environment);

Object* clisp_make_lambda_without_env(clisp_func func);

void destroy_lambda(Object* object);

Object* clisp_lambda_call(Object* obj, CLISP_FUNC_PARAMS);
