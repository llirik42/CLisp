#include "objects/lambda.h"

#include "lib/memory.h"
#include "lib/utils.h"
#include "vector.h"

#include <stdarg.h>

CL_Object* cl_make_lambda(cl_func_with_env func, CL_Environment* environment) {
    CL_LambdaUserObject* lambda_object = cl_allocate_memory(sizeof(CL_LambdaUserObject));
    cl_init_obj((CL_Object*)lambda_object, LAMBDA);

    lambda_object->cl_func = func;
    lambda_object->lambda_type = USER;
    lambda_object->environment = environment;
    lambda_object->call_environments = cl_da_create(UNDEFINED_DA_CAPACITY);
    cl_inc_env_refs_cnt(environment);
    return (CL_Object*)lambda_object;
}

CL_Object* cl_make_lambda_without_env(cl_func func) {
    CL_LambdaLibraryObject* lambda_object = cl_allocate_memory(sizeof(CL_LambdaLibraryObject));
    cl_init_obj((CL_Object*)lambda_object, LAMBDA);

    lambda_object->cl_func = func;
    lambda_object->lambda_type = LIBRARY;
    return (CL_Object*)lambda_object;
}

CL_Object* cl_make_lambda_native(cl_func_native func, CL_NativeData* data) {
    CL_LambdaNativeObject* lambda_object = cl_allocate_memory(sizeof(CL_LambdaNativeObject));
    cl_init_obj((CL_Object*)lambda_object, LAMBDA);

    lambda_object->cl_func = func;
    lambda_object->lambda_type = NATIVE;
    lambda_object->native_data = data;
    return (CL_Object*)lambda_object;
}

void cl_destroy_lambda(CL_Object* obj) {
    CL_LambdaObject* lambda_object = (CL_LambdaObject*)obj;
    switch (lambda_object->lambda_type) {
        case USER: {
            CL_LambdaUserObject* lambda_user = (CL_LambdaUserObject*)lambda_object;
            CL_DynamicArray* call_envs = lambda_user->call_environments;

            for (size_t i = 0; i < cl_da_size(call_envs); i++) {
                CL_Environment* call_env = cl_da_get(call_envs, i);
                cl_dec_env_refs_cnt(call_env);
            }

            cl_da_destroy(call_envs);
            cl_dec_env_refs_cnt(lambda_user->environment);
            break;
        }
        case NATIVE: {
            CL_LambdaNativeObject* lambda_native = (CL_LambdaNativeObject*)lambda_object;
            cl_destroy_native_data(lambda_native->native_data);
            break;
        }
        default: {}
    }

    cl_free_memory(obj);
}

static CL_Object* cl_lambda_call_array(CL_Object* obj, CL_FUNC_PARAMS) {
    const CL_LambdaObject* lambda_object = (CL_LambdaObject*)obj;
    switch (lambda_object->lambda_type) {
        case USER: {
            CL_LambdaUserObject* lambda_user = (CL_LambdaUserObject*)lambda_object;
            CL_Environment* lambda_call_env = cl_make_env(lambda_user->environment);
            cl_da_append(lambda_user->call_environments, lambda_call_env);
            return lambda_user->cl_func(lambda_call_env, CL_FUNC_PARAMS_WITHOUT_TYPES);
        }
        case NATIVE: {
            CL_LambdaNativeObject* lambda_native = (CL_LambdaNativeObject*)lambda_object;
            return lambda_native->cl_func(lambda_native->native_data, CL_FUNC_PARAMS_WITHOUT_TYPES);
        }
        case LIBRARY: {
            CL_LambdaLibraryObject* lambda_native = (CL_LambdaLibraryObject*)lambda_object;
            return lambda_native->cl_func(CL_FUNC_PARAMS_WITHOUT_TYPES);
        }
        default:
            __builtin_unreachable();
    }
}

CL_Object* cl_lambda_call(CL_Object* obj, unsigned int count, ...) {
    // The function is called by an ordinary procedure call

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
    // The function is called by (apply ...)

    va_list args;
    va_start(args, count);
    CL_Object* tmp[count];
    for (unsigned int i = 0; i < count; i++) {
        tmp[i] = va_arg(args, CL_Object*);
    }
    va_end(args);

    unsigned int scalar_args_count = count - 1;
    CL_Object* list_arg = tmp[scalar_args_count];
    CL_CHECK_FUNC_ARG_TYPE(cl_get_obj_type(list_arg), VECTOR);

    unsigned int list_arg_length = cl_vector_length(list_arg);
    unsigned int obj_args_count = scalar_args_count + list_arg_length;
    CL_Object* obj_args[obj_args_count];
    for (unsigned int i = 0; i < scalar_args_count; i++) {
        obj_args[i] = tmp[i];
    }
    for (unsigned int i = 0; i < list_arg_length; i++) {
        obj_args[i + scalar_args_count] = cl_vector_at(list_arg, i);
    }

    CL_Object* result = cl_lambda_call_array(obj, obj_args_count, obj_args);
    return result;
}
