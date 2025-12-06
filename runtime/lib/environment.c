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
    cl_func func;
} NamedFunc;

static const NamedFunc reserved[] = {
    {"display", cl_display},
    {"+", cl_add},
    {"-", cl_sub},
    {"*", cl_mul},
    {"/", cl_div},
    {">", cl_greater},
    {">=", cl_greater_or_equal},
    {"<", cl_less},
    {"<=", cl_less_or_equal},
    {"=", cl_equal},
    {"not", cl_not},
};

#define RESERVED_COUNT sizeof(reserved) / sizeof(NamedFunc)

static CL_Environment* make_environment(CL_Environment* parent, size_t capacity) {
    CL_Environment* env = cl_allocate_memory(sizeof(CL_Environment));
    env->parent = parent;
    env->capacity = capacity;
    env->variables_count = 0;
    env->ref_count = 1;
    env->variables = cl_allocate_memory(sizeof(CL_Variable) * capacity);
    return env;
}

static void destroy_env(CL_Environment* env) {
    for (size_t i = 0; i < env->variables_count; i++) {
        cl_decrease_ref_count(env->variables[i].val);
    }
    cl_free_memory(env->variables);
    cl_free_memory(env);
}

CL_Environment* cl_make_env(CL_Environment* parent) {
    return make_environment(parent, BASIC_CAPACITY);
}

CL_Environment* cl_make_env_capacity(CL_Environment* parent, size_t capacity) {
    return make_environment(parent, capacity);
}

void cl_inc_env_refs_cnt(CL_Environment* env) {
    env->ref_count++;
}

void cl_dec_env_refs_cnt(CL_Environment* env) {
    if (!env || --env->ref_count > 0) {
        return;
    }
    destroy_env(env);
}

void cl_set_variable_value(CL_Environment* env, char* name, CL_Object* value) {
    if (!env) {
        cl_abort("Environment is NULL!\n");
        __builtin_unreachable();
    }

    cl_increase_ref_count(value);

    for (size_t i = 0; i < env->variables_count; i++) {
        CL_Variable* var = &env->variables[i];
        if (!strcmp(name, var->key)) {
            cl_decrease_ref_count(var->val);
            var->val = value;
            return;
        }
    }

    if (env->variables_count >= env->capacity) {
        env->capacity = (int)ceil((double)env->capacity * CAPACITY_MULTIPLIER);
        env->variables = cl_reallocate_memory(env->variables, sizeof(CL_Variable) * env->capacity);
    }

    CL_Variable var = {name, value};
    env->variables[env->variables_count++] = var;
}

CL_Object* cl_update_variable_value(CL_Environment* env, char* name, CL_Object* value) {
    if (!env) {
        cl_abort("Environment is NULL!\n");
        __builtin_unreachable();
    }

    cl_increase_ref_count(value);

    CL_Environment* curr_env = env;
    while (curr_env) {
        for (size_t i = 0; i < curr_env->variables_count; i++) {
            CL_Variable* var = &curr_env->variables[i];
            if (!strcmp(name, var->key)) {
                cl_decrease_ref_count(var->val);
                var->val = value;
                return cl_make_unspecified();
            }
        }

        curr_env = curr_env->parent;
    }

    cl_abort("No value in environment!\n");
    __builtin_unreachable();
}

CL_Object* cl_get_variable_value(CL_Environment* env, char* name) {
    CL_Environment* curr_env = env;

    while (curr_env) {
        for (size_t i = 0; i < curr_env->variables_count; i++) {
            if (!strcmp(name, curr_env->variables[i].key)) {
                return curr_env->variables[i].val;
            }
        }

        curr_env = curr_env->parent;
    }

    cl_abort("No value in environment!\n");
    __builtin_unreachable();
}

static void set_reserved_variable(CL_Environment* env, const char* name, CL_Object* value) {
    CL_Variable var = {name, value};
    env->variables[env->variables_count++] = var;
}

CL_Environment* cl_make_global_env() {
    CL_Environment* env = cl_make_env_capacity(NULL, RESERVED_COUNT);
    for (size_t i = 0; i < RESERVED_COUNT; i++) {
        set_reserved_variable(env, reserved[i].name, cl_make_lambda_without_env(reserved[i].func));
    }

    return env;
}

void cl_destroy_global_env(CL_Environment* env) {
    destroy_env(env);
}

CL_Environment* cl_move_env(CL_Environment* env) {
    CL_Environment* new = cl_allocate_memory(sizeof(CL_Environment));
    new->variables_count = env->variables_count;
    new->capacity = env->capacity;
    new->ref_count = 1;
    new->parent = env->parent;

    if (new->variables_count) {
        new->variables = cl_allocate_memory(sizeof(CL_Variable) * new->variables_count);
        memcpy(new->variables, env->variables, sizeof(CL_Variable) * new->variables_count);
    } else {
        new->variables = cl_allocate_memory(sizeof(CL_Variable) * BASIC_CAPACITY);
    }

    for (unsigned int i = 0; i < new->variables_count; i++) {
        cl_increase_ref_count(new->variables[i].val);
    }

    cl_dec_env_refs_cnt(env);

    return new;
}
