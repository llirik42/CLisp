#include "environment.h"

#include <math.h>
#include <string.h>

#include "arithmetic.h"
#include "comparation.h"
#include "core.h"
#include "io.h"
#include "logic.h"
#include "memory.h"
#include "utils.h"
#include "objects/lambda.h"

#define BASIC_CAPACITY 4
#define CAPACITY_MULTIPLIER 1.5

typedef struct NamedFunc {
    const char* name;
    clisp_func func;
} NamedFunc;

static const NamedFunc reserved[] = {
    {"display", clisp_display},
    {"+", clisp_add},
    {"-", clisp_sub},
    {"*", clisp_mul},
    {"/", clisp_div},
    {">", clisp_greater},
    {">=", clisp_greater_or_equal},
    {"<", clisp_less},
    {"<=", clisp_less_or_equal},
    {"==", clisp_equal},
    {"not", clisp_not},
};

#define RESERVED_COUNT sizeof(reserved) / sizeof(NamedFunc)

static Environment* make_environment(Environment* parent, size_t capacity) {
    Environment* env = allocate_memory(sizeof(Environment));
    env->parent = parent;
    env->capacity = capacity;
    env->variables_count = 0;
    env->variables = allocate_memory(sizeof(Variable) * capacity);
    return env;
}

Environment* clisp_make_environment(Environment* parent) {
    return make_environment(parent, BASIC_CAPACITY);
}

Environment* clisp_make_environment_capacity(Environment* parent, size_t capacity) {
    return make_environment(parent, capacity);
}

void clisp_destroy_environment(Environment* env) {
    free_memory(env->variables);
    free_memory(env);
}

void clisp_set_variable_value(Environment* env, char* name, Object* value) {
    if (!env) {
        print_error_and_exit("Environment is NULL!\n", 0);
        __builtin_unreachable();
    }

    for (size_t i = 0; i < RESERVED_COUNT; i++) {
        if (!strcmp(name, reserved[i].name)) {
            print_error_and_exit("Variable name is reserved!\n", 0);
        }
    }

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
        print_error_and_exit("Environment is NULL!\n", 0);
        __builtin_unreachable();
    }

    for (size_t i = 0; i < RESERVED_COUNT; i++) {
        if (!strcmp(name, reserved[i].name)) {
            print_error_and_exit("Variable name is reserved!\n", 0);
        }
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
        print_error_and_exit("Environment is NULL!\n", 0);
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

static void set_reserved_variable(Environment* env, const char* name, Object* value) {
    Variable var = {name, value};
    env->variables[env->variables_count++] = var;
}

Environment* clisp_make_global_environment() {
    Environment* env = clisp_make_environment_capacity(NULL, RESERVED_COUNT);
    for (size_t i = 0; i < RESERVED_COUNT; i++) {
        set_reserved_variable(env, reserved[i].name, clisp_make_lambda_without_env(reserved[i].func));
    }

    return env;
}

void clisp_destroy_global_environment(Environment* env) {
    for (size_t i = 0; i < RESERVED_COUNT; i++) {
        clisp_destroy_object(env->variables[i].val);
    }

    clisp_destroy_environment(env);
}
