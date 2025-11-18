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

Environment* clisp_make_environment(Environment* parent, size_t capacity);

void clisp_destroy_environment(Environment* env);

void set_variable_value(Environment* env, char* name, Object* value);

Object* update_variable_value(Environment* env, char* name, Object* value);

Object* get_variable_value(Environment* env, char* name);
