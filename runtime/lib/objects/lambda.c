#include "objects/lambda.h"

#include "lib/memory.h"

CL_Object* cl_make_lambda(cl_func_with_env func, CL_Environment* environment) {
    CL_LambdaObject* lambda_object = cl_allocate_memory(sizeof(CL_LambdaObject));
    cl_init_obj((CL_Object*)lambda_object, LAMBDA);

    lambda_object->func.cl_func_with_env = func;
    lambda_object->with_env = TRUE;
    lambda_object->environment = cl_make_env(environment);
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

        for (size_t i = 0; i < call_envs->size; i++) {
            CL_Environment* call_env = cl_da_get(call_envs, i);
            cl_destroy_env(call_env);
        }

        cl_da_destroy(call_envs);
    }
    cl_free_memory(obj);
}

CL_Object* cl_lambda_call(CL_Object* obj, CL_FUNC_PARAMS) {
    const CL_LambdaObject* lambda_object = (CL_LambdaObject*)obj;
    if (lambda_object->with_env) {
        CL_Environment* lambda_call_env = cl_make_env(lambda_object->environment);
        cl_da_append(lambda_object->call_environments, lambda_call_env);
        return lambda_object->func.cl_func_with_env(lambda_call_env, CL_FUNC_PARAMS_WITHOUT_TYPES);
    }
    return lambda_object->func.cl_func(CL_FUNC_PARAMS_WITHOUT_TYPES);
}
