#include "evaluable.h"

#include <stdarg.h>
#include <stdio.h>
#include <stdlib.h>

#include "memory.h"

Object* make_evaluable(Object* (*func)(unsigned int, Object**), unsigned int count, Object** args) {
    FunctionWrapper* wrapper = allocate_memory(sizeof(FunctionWrapper));

    wrapper->args_count = count;
    wrapper->function = func;
    wrapper->args = args;

    Object* obj = allocate_memory(sizeof(Object));

    obj->type = EVALUABLE;
    obj->value = wrapper;
    return obj;
}

Object* evaluate(Object* function_wrapper_obj) {
    if (function_wrapper_obj->type != EVALUABLE) {
        fprintf(stderr, "evaluate: function_wrapper is not EVALUABLE\n");
        exit(EXIT_FAILURE);
    }

    const FunctionWrapper* wrapper = function_wrapper_obj->value;

    return wrapper->function(wrapper->args_count, wrapper->args);
}
