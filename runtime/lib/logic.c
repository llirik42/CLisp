#include "logic.h"

#include <stdio.h>

#include "objects/primitive.h"
#include "utils.h"

CL_Object* cl_if(CL_FUNC_PARAMS) {
    if (count < 1 || count > 3) {
        char error[CL_ERROR_BUF_SIZE];
        snprintf(error, sizeof(error), "Invalid number of arguments passed to clisp_if! Expected 2 or 3. Got %d\n", count);
        cl_abort(error);
    }

    unsigned char test_value = cl_obj_to_boolean(args[0]);

    if (test_value) {
        CL_Object* consequent = cl_unwrap_obj(args[1]);
        if (consequent == args[1]) {
            cl_increase_refs_count(consequent);
        }
        return consequent;
    }

    if (count == 2) {
        return cl_make_unspecified();
    }

    CL_Object* alternative = cl_unwrap_obj(args[2]);
    if (alternative == args[2]) {
        cl_increase_refs_count(alternative);
    }
    return alternative;
}

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

CL_Object* cl_or(CL_FUNC_PARAMS) {
    if (count == 0) {
        return cl_make_false();
    }

    for (unsigned int i = 0; i < count - 1; i++) {
        CL_Object* statement = cl_unwrap_obj(args[i]);
        unsigned char statement_value = cl_obj_to_boolean(statement);
        cl_destroy_if_unwrapped(args[i], statement);
        // 1 v A = 1
        if (statement_value) {
            return cl_make_true();
        }
    }

    CL_Object* last_statement = cl_unwrap_obj(args[count - 1]);
    unsigned char statement_value = cl_obj_to_boolean(last_statement);
    cl_destroy_if_unwrapped(args[count - 1], last_statement);
    if (statement_value) {
        return cl_make_true();
    }

    return cl_make_false();
}

CL_Object* cl_and(CL_FUNC_PARAMS) {
    if (count == 0) {
        return cl_make_true();
    }

    for (unsigned int i = 0; i < count - 1; i++) {
        CL_Object* statement = cl_unwrap_obj(args[i]);
        unsigned char statement_value = cl_obj_to_boolean(statement);
        cl_destroy_if_unwrapped(args[i], statement);

        // 0 & A = 1
        if (!statement_value) {
            return cl_make_false();
        }
    }

    CL_Object* last_statement = cl_unwrap_obj(args[count - 1]);
    unsigned char statement_value = cl_obj_to_boolean(last_statement);
    cl_destroy_if_unwrapped(args[count - 1], last_statement);

    if (statement_value) {
        return cl_make_true();
    }

    return cl_make_false();
}
