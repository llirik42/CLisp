#pragma once
#include "core.h"
#include "data_objects/dynamic_array.h"

typedef struct {
    const char* key;
    CL_Object* val;
} CL_Variable;

typedef struct Environment {
    struct Environment* parent;
    CL_Variable* variables;
    size_t variables_count;
    size_t capacity;
} CL_Environment;

CL_Environment* cl_make_env(CL_Environment* parent);

CL_Environment* cl_make_env_capacity(CL_Environment* parent, size_t capacity);

void cl_destroy_env(CL_Environment* env);

void cl_set_variable_value(CL_Environment* env, char* name, CL_Object* value);

CL_Object* cl_update_variable_value(CL_Environment* env, char* name, CL_Object* value);

CL_Object* cl_get_variable_value(CL_Environment* env, char* name);

CL_Environment* cl_make_global_env();

void cl_destroy_global_env(CL_Environment* env);
