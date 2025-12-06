#include "objects/lambda.h"

#include "lib/memory.h"
#include "list.h"

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

static CL_Object* cl_lambda_call_array(CL_Object* obj, CL_FUNC_PARAMS) {
    const CL_LambdaObject* lambda_object = (CL_LambdaObject*)obj;
    if (lambda_object->with_env) {
        CL_Environment* lambda_call_env = cl_make_env(lambda_object->environment);
        cl_da_append(lambda_object->call_environments, lambda_call_env);
        return lambda_object->func.cl_func_with_env(lambda_call_env, CL_FUNC_PARAMS_WITHOUT_TYPES);
    }
    return lambda_object->func.cl_func(CL_FUNC_PARAMS_WITHOUT_TYPES);
}

CL_Object* cl_lambda_call(CL_Object* obj, unsigned int count, ...) {
    va_list args;
    va_start(args, count);
    CL_Object* obj_args[count];
    for (unsigned int i = 0; i < count; i++) {
        obj_args[i] = va_arg(args, CL_Object*);
    }
    va_end(args);

    CL_Object* result = cl_lambda_call_array(obj, count, obj_args);
    return result;
}

CL_Object* cl_lambda_call_list(CL_Object* obj, unsigned int count, ...) {
    va_list args;
    va_start(args, count);
    CL_Object* tmp[count];
    for (unsigned int i = 0; i < count; i++) {
        tmp[i] = va_arg(args, CL_Object*);
    }
    va_end(args);

    unsigned int scalar_args_count = count - 1;
    CL_Object* list_arg = tmp[scalar_args_count];
    unsigned int list_arg_length = cl_list_length(list_arg);
    unsigned int obj_args_count = scalar_args_count + list_arg_length;
    CL_Object* obj_args[obj_args_count];
    for (unsigned int i = 0; i < scalar_args_count; i++) {
        obj_args[i] = tmp[i];
    }
    for (unsigned int i = 0; i < list_arg_length; i++) {
        obj_args[i + scalar_args_count] = cl_list_at(list_arg, i);
    }

    CL_Object* result = cl_lambda_call_array(obj, obj_args_count, obj_args);
    return result;
}
