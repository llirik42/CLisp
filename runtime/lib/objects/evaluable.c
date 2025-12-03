#include "evaluable.h"

#include "memory.h"
#include "utils.h"

CL_Object* cl_make_evaluable(cl_evaluable_func func, CL_Environment* env) {
    CL_EvaluableObject* evaluable_object = cl_allocate_memory(sizeof(CL_EvaluableObject));
    cl_init_obj((CL_Object*)evaluable_object, EVALUABLE);

    evaluable_object->function = func;
    evaluable_object->environment = env;
    evaluable_object->result = NULL;
    return (CL_Object*)evaluable_object;
}

void cl_destroy_evaluable(CL_Object* obj) {
    cl_free_memory(obj);
}

CL_Object* cl_evaluate(CL_Object* obj) {
    // TODO: uncomment this after dealing with cl_unwrap_obj()
//    if (cl_get_obj_type(obj) != EVALUABLE) {
//        cl_abort("Object is not evaluable!\n");
//        __builtin_unreachable();
//    }

    if (cl_get_obj_type(obj) != EVALUABLE) {
        return obj;
    }

    CL_EvaluableObject* evaluable_object = (CL_EvaluableObject*)obj;

    if (evaluable_object->result != NULL) {
        return evaluable_object->result;
    }

    CL_Object* result = evaluable_object->function(evaluable_object->environment);
    evaluable_object->result = result;

    return result;
}
