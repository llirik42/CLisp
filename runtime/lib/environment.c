#include "environment.h"

#include <math.h>
#include <string.h>

#include "core.h"
#include "memory.h"
#include "utils.h"

#define BASIC_CAPACITY 4
#define CAPACITY_MULTIPLIER 1.5

static Environment* make_environment_base(Environment* parent, size_t capacity) {
    Environment* env = allocate_memory(sizeof(Environment));
    env->parent = parent;
    env->capacity = capacity;
    env->variables_count = 0;
    env->variables = allocate_memory(sizeof(Variable) * capacity);
    return env;
}

Environment* clisp_make_environment(Environment* parent) {
    return make_environment_base(parent, BASIC_CAPACITY);
}

Environment* clisp_make_environment_capacity(Environment* parent, size_t capacity) {
    return make_environment_base(parent, capacity);
}

void clisp_destroy_environment(Environment* env) {
    free_memory(env->variables);
    free_memory(env);
}

void clisp_set_variable_value(Environment* env, char* name, Object* value) {
    for (size_t i = 0; i < env->variables_count; i++) {
        if (!strcmp(name, env->variables[i].key)) {
            env->variables[i].val = value;
            return;
        }
    }

    if (env->variables_count >= env->capacity) {
        env->capacity = (int)ceil((double)env->capacity * CAPACITY_MULTIPLIER);
        env->variables = reallocate_memory(env->variables, sizeof(Variable) * env->capacity);
    }

    Variable var = {name, value};
    env->variables[env->variables_count++] = var;
}

Object* clisp_update_variable_value(Environment* env, char* name, Object* value) {
    if (!env) {
        print_error_and_exit("No variable in environment!\n", 0);
        __builtin_unreachable();
    }

    for (size_t i = 0; i < env->variables_count; i++) {
        if (!strcmp(name, env->variables[i].key)) {
            env->variables[i].val = value;
            return clisp_make_unspecified();
        }
    }
    return clisp_update_variable_value(env->parent, name, value);
}

Object* clisp_get_variable_value(Environment* env, char* name) {
    if (!env) {
        print_error_and_exit("No variable in environment!\n", 0);
        __builtin_unreachable();
    }

    for (size_t i = 0; i < env->variables_count; i++) {
        Variable var = env->variables[i];
        if (!strcmp(name, var.key)) {
            return var.val;
        }
    }
    return clisp_get_variable_value(env->parent, name);
}
