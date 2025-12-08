#include "logic.h"

#include "utils.h"

#include "lib/objects/primitive.h"

CL_Object* cl_not(CL_FUNC_PARAMS) {
    CL_CHECK_FUNC_ARGS_COUNT(count, 1, EQUAL);

    CL_Object* term = args[0];
    bool term_value = cl_obj_to_boolean(term);

    if (term_value) {
        return cl_make_false();
    }
    return cl_make_true();
}
