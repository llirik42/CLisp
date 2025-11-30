#include "evaluable.h"

#include "memory.h"

CL_Object* cl_make_evaluable(cl_func func, CL_FUNC_PARAMS) {
    CL_EvaluableObject* evaluable_object = allocate_memory(sizeof(CL_EvaluableObject));
    cl_init_obj((CL_Object*)evaluable_object, EVALUABLE);

    evaluable_object->args_count = count;
    evaluable_object->function = func;
    evaluable_object->args = args;

    return (CL_Object*)evaluable_object;
}

void cl_destroy_evaluable(CL_Object* obj) {
    free_memory(obj);
}

CL_Object* cl_evaluate(CL_Object* obj) {
    if (cl_get_obj_type(obj) != EVALUABLE) {
        return obj;
    }

    const CL_EvaluableObject* evaluable_object = (CL_EvaluableObject*)obj;

    return evaluable_object->function(evaluable_object->args_count, evaluable_object->args);
}
