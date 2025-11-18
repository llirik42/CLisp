#include "environment.h"

#include <math.h>
#include <string.h>

#include "core.h"
#include "memory.h"
#include "utils.h"

#define BASIC_CAPACITY 4

Environment* make_environment(Environment* parent, size_t capacity) {
    if (!capacity) {
        capacity = BASIC_CAPACITY;
    }

    Environment* env = allocate_memory(sizeof(Environment));
    env->parent = parent;
    env->capacity = capacity;
    env->variables_count = 0;
    env->variables = allocate_memory(sizeof(Variable) * capacity);
    return env;
}

void destroy_environment(Environment* env) {
    free_memory(env->variables);
    free_memory(env);
}

void set_variable_value(Environment* env, char* name, Object* value) {
    for (size_t i = 0; i < env->variables_count; i++) {
        if (!strcmp(name, env->variables[i].key)) {
            env->variables[i].val = value;
            return;
        }
    }

    if (env->variables_count >= env->capacity) {
        env->capacity = (int)ceil((double)env->capacity * 1.5);
        env->variables = reallocate_memory(env->variables, sizeof(Variable) * env->capacity);
    }

    Variable var = {name, value};
    env->variables[env->variables_count++] = var;
}

Object* update_variable_value(Environment* env, char* name, Object* value) {
    if (!env) {
        print_error_and_exit("No variable in environment!\n", 0);
        __builtin_unreachable();
    }

    for (size_t i = 0; i < env->variables_count; i++) {
        if (!strcmp(name, env->variables[i].key)) {
            env->variables[i].val = value;
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

    for (size_t i = 0; i < env->variables_count; i++) {
        Variable var = env->variables[i];
        if (!strcmp(name, var.key)) {
            return var.val;
        }
    }
    return get_variable_value(env->parent, name);
}
