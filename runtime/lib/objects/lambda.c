#include "objects/lambda.h"

#include "lib/memory.h"

#include <stdarg.h>

CL_Object* cl_make_lambda(cl_func_with_env func, CL_Environment* environment) {
    CL_LambdaObject* lambda_object = cl_allocate_memory(sizeof(CL_LambdaObject));
    cl_init_obj((CL_Object*)lambda_object, LAMBDA);

    lambda_object->func.cl_func_with_env = func;
    lambda_object->with_env = TRUE;
    lambda_object->environment = environment;
    lambda_object->call_environments = cl_da_create(UNDEFINED_DA_CAPACITY);
    return (CL_Object*)lambda_object;
}

CL_Object* cl_make_lambda_without_env(cl_func func) {
    CL_LambdaObject* lambda_object = cl_allocate_memory(sizeof(CL_LambdaObject));
    cl_init_obj((CL_Object*)lambda_object, LAMBDA);

    lambda_object->func.cl_func = func;
    lambda_object->with_env = FALSE;
    lambda_object->call_environments = NULL;
    return (CL_Object*)lambda_object;
}

void cl_destroy_lambda(CL_Object* obj) {
    CL_LambdaObject* lambda_object = (CL_LambdaObject*)obj;
    if (lambda_object->with_env) {
        CL_DynamicArray* call_envs = lambda_object->call_environments;

        for (size_t i = 0; i < cl_da_size(call_envs); i++) {
            CL_Environment* call_env = cl_da_get(call_envs, i);
            cl_destroy_env(call_env);
        }

        cl_da_destroy(call_envs);
    }
    cl_free_memory(obj);
}

CL_Object* cl_lambda_call(CL_Object* obj, unsigned int count, unsigned int scalar_count, ...) {
    const CL_LambdaObject* lambda_object = (CL_LambdaObject*)obj;

    va_list args;
    va_start(args, scalar_count);

    unsigned int obj_args_count = count;  // TODO:
    CL_Object* obj_args[obj_args_count];
    for (unsigned int i = 0; i < scalar_count; i++) {
        obj_args[i] = va_arg(args, CL_Object*);
    }

    CL_Object* result;
    if (lambda_object->with_env) {
        CL_Environment* lambda_call_env = cl_make_env(lambda_object->environment);
        cl_da_append(lambda_object->call_environments, lambda_call_env);
        result = lambda_object->func.cl_func_with_env(lambda_call_env, obj_args_count, obj_args);
    }
    else {
        result = lambda_object->func.cl_func(obj_args_count, obj_args);
    }

    va_end(args);
    return result;
}
