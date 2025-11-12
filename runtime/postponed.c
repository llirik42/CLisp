#include "postponed.h"
#include "utils.h"

#include <stdarg.h>
#include <stdio.h>
#include <stdlib.h>

Object* make_evaluable(Object* (*func)(int, Object**), int count, Object** args) {
    FunctionWrapper* wrapper = malloc(sizeof(FunctionWrapper));
    check_allocated(wrapper);

    wrapper->args_count = count;
    wrapper->function = func;
    wrapper->args = args;

    Object* obj = malloc(sizeof(Object));
    check_allocated(obj);

    obj->type = POSTPONED;
    obj->value = wrapper;
    return obj;
}

Object* evaluate(const Object* function_wrapper_obj) {
    if (function_wrapper_obj->type != POSTPONED) {
        fprintf(stderr, "evaluate: function_wrapper is not POSTPONED");
        exit(EXIT_FAILURE);
    }

    const FunctionWrapper* wrapper = function_wrapper_obj->value;

    return wrapper->function(wrapper->args_count, wrapper->args);
}