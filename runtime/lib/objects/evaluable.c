#include "evaluable.h"

#include "lib/memory/memory.h"
#include "lib/core/utils.h"

CL_Object* cl_make_evaluable(cl_evaluable_func func, CL_Environment* env) {
    CL_EvaluableObject* evaluable_object = cl_allocate_memory(sizeof(CL_EvaluableObject));
    cl_init_obj((CL_Object*)evaluable_object, EVALUABLE);

    evaluable_object->function = func;
    evaluable_object->environment = env;
    evaluable_object->result = NULL;
    cl_inc_env_refs_cnt(evaluable_object->environment);
    return (CL_Object*)evaluable_object;
}

void cl_destroy_evaluable(CL_Object* obj) {
    CL_EvaluableObject* evaluable_object = (CL_EvaluableObject*)obj;
    if (evaluable_object->result) {
        cl_dec_refs_cnt(evaluable_object->result);
    }

    cl_free_memory(obj);
}

CL_Object* cl_evaluate(CL_Object* obj) {
    CL_CHECK_FUNC_ARG_TYPE(cl_get_obj_type(obj), EVALUABLE);

    CL_EvaluableObject* evaluable_object = (CL_EvaluableObject*)obj;

    if (evaluable_object->result != NULL) {
        cl_inc_refs_cnt(evaluable_object->result);
        return evaluable_object->result;
    }

    CL_Object* result = evaluable_object->function(evaluable_object->environment);
    evaluable_object->result = result;
    cl_dec_env_refs_cnt(evaluable_object->environment);
    cl_inc_refs_cnt(evaluable_object->result);

    return result;
}
