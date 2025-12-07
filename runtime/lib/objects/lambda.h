#pragma once
#include "lib/native_calls.h"
#include "lib/environment.h"
#include "lib/core.h"

typedef CL_Object*(*cl_func_with_env)(CL_Environment* env, CL_FUNC_PARAMS);
typedef CL_Object*(*cl_func_native)(CL_NativeData* data, CL_FUNC_PARAMS);

enum CL_LambdaType {
    USER,
    LIBRARY,
    NATIVE,
};

typedef struct {
    enum CL_ObjectType type;
    unsigned short ref_count;
    enum CL_LambdaType lambda_type;
} CL_LambdaObject;

typedef struct {
    enum CL_ObjectType type;
    unsigned short ref_count;
    enum CL_LambdaType lambda_type;
    cl_func_with_env cl_func;
    CL_Environment* environment;
    CL_DynamicArray* call_environments;
} CL_LambdaUserObject;

typedef struct {
    enum CL_ObjectType type;
    unsigned short ref_count;
    enum CL_LambdaType lambda_type;
    cl_func cl_func;
} CL_LambdaLibraryObject;

typedef struct {
    enum CL_ObjectType type;
    unsigned short ref_count;
    enum CL_LambdaType lambda_type;
    cl_func_native cl_func;
    CL_NativeData* native_data;
} CL_LambdaNativeObject;

CL_Object* cl_make_lambda(cl_func_with_env func, CL_Environment* environment);

CL_Object* cl_make_lambda_without_env(cl_func func);

CL_Object* cl_make_lambda_native(cl_func_native func, CL_NativeData* data);

void cl_destroy_lambda(CL_Object* object);

CL_Object* cl_lambda_call(CL_Object* obj, unsigned int count, ...);

CL_Object* cl_lambda_call_list(CL_Object* obj, unsigned int count, ...);
