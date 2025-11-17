#include "environment.h"

#include <string.h>

#include "core.h"
#include "memory.h"
#include "utils.h"

typedef struct {
    char* key;
    Object* val;
} Variable;

Environment* make_environment(Environment* parent) {
    Environment* env = allocate_memory(sizeof(Environment));
    env->parent = parent;
    env->variables = da_create();
    return env;
}

void destroy_environment(Environment* env) {
    for (size_t i = 0; i < da_size(env->variables); i++) {
        free_memory(da_get(env->variables, i));
    }
    da_destroy(env->variables);
    free_memory(env);
}

void set_variable_value(Environment* env, char* name, Object* value) {
    Variable* var = allocate_memory(sizeof(Variable));
    var->key = name;
    var->val = value;
    da_push_back(env->variables, var);
}

Object* update_variable_value(Environment* env, char* name, Object* value) {
    if (!env) {
        print_error_and_exit("No variable in environment!\n", 0);
        __builtin_unreachable();
    }

    for (size_t i = 0; i < da_size(env->variables); i++) {
        Variable* var = da_get(env->variables, i);
        if (!strcmp(name, var->key)) {
            var->val = value;
            return make_unspecified();
        }
    }
    return update_variable_value(env->parent, name, value);
}

Object* get_variable_value(Environment* env, char* name) {
    if (!env) {
        print_error_and_exit("No variable in environment!\n", 0);
        __builtin_unreachable();
    }

    for (size_t i = 0; i < da_size(env->variables); i++) {
        Variable* var = da_get(env->variables, i);
        if (!strcmp(name, var->key)) {
            return var->val;
        }
    }
    return get_variable_value(env->parent, name);
}
