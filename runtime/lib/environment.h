#pragma once
#include "core.h"
#include "data_objects/dynamic_array.h"

typedef struct {
    char* key;
    Object* val;
} Variable;

typedef struct Environment {
    struct Environment* parent;
    Variable* variables;
    size_t variables_count;
    size_t capacity;
} Environment;

Environment* clisp_make_environment(Environment* parent);

Environment* clisp_make_environment_capacity(Environment* parent, size_t capacity);

void clisp_destroy_environment(Environment* env);

void clisp_set_variable_value(Environment* env, char* name, Object* value);

Object* clisp_update_variable_value(Environment* env, char* name, Object* value);

Object* clisp_get_variable_value(Environment* env, char* name);
