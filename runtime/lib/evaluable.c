#include "evaluable.h"

#include "memory.h"

Object* make_evaluable(postponed_func func, CLISP_FUNC_PARAMS) {
    FunctionWrapper* wrapper = allocate_memory(sizeof(FunctionWrapper));

    wrapper->args_count = count;
    wrapper->function = func;
    wrapper->args = args;
    wrapper->type = EVALUABLE;

    return (Object*)wrapper;
}

void destroy_evaluable(Object* obj) {
    free_memory(obj);
}

Object* evaluate(Object* obj) {
    if (get_object_type(obj) != EVALUABLE) {
        return obj;
    }

    const FunctionWrapper* wrapper = (FunctionWrapper*)obj;

    return wrapper->function(wrapper->args_count, wrapper->args);
}
