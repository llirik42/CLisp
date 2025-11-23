#include "evaluable.h"

#include "../memory.h"

Object* clisp_make_evaluable(postponed_func func, CLISP_FUNC_PARAMS) {
    EvaluableObject* evaluable_object = allocate_memory(sizeof(EvaluableObject));
    init_object((Object*)evaluable_object, EVALUABLE);

    evaluable_object->args_count = count;
    evaluable_object->function = func;
    evaluable_object->args = args;

    return (Object*)evaluable_object;
}

void destroy_evaluable(Object* obj) {
    free_memory(obj);
}

Object* evaluate(Object* obj) {
    if (get_object_type(obj) != EVALUABLE) {
        return obj;
    }

    const EvaluableObject* evaluable_object = (EvaluableObject*)obj;

    return evaluable_object->function(evaluable_object->args_count, evaluable_object->args);
}
