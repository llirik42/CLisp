#include "logic.h"

#include <stdio.h>

#include "objects/primitive.h"
#include "utils.h"

CL_Object* cl_not(CL_FUNC_PARAMS) {
    CL_CHECK_FUNC_ARGS_COUNT(count, 1, EQUAL);

    CL_Object* term = cl_unwrap_obj(args[0]);
    unsigned char term_value = cl_obj_to_boolean(term);
    cl_destroy_if_unwrapped(args[0], term);

    if (term_value) {
        return cl_make_false();
    }
    return cl_make_true();
}
