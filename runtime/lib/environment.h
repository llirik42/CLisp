#pragma once
#include "core.h"
#include "data_objects/dynamic_array.h"

typedef struct Environment {
    struct Environment* parent;
    DynamicArray* variables;
} Environment;

Environment* make_environment(Environment* parent);

void destroy_environment(Environment* env);

void set_variable_value(Environment* env, char* name, Object* value);

Object* update_variable_value(Environment* env, char* name, Object* value);

Object* get_variable_value(Environment* env, char* name);
