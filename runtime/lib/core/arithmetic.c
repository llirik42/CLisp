#include "arithmetic.h"

#include <stddef.h>

#include "utils.h"

#include "lib/objects/primitive.h"
#include "lib/exit/abort.h"
#include "lib/objects/primitive_types.h"

static void set_int_value(CL_Object* obj, int new_value) {
    CL_IntObject* int_object = (CL_IntObject*)obj;
    int_object->value = new_value;
}

static void set_double_value(CL_Object* obj, double new_value) {
    CL_DoubleObject* double_object = (CL_DoubleObject*)obj;
    double_object->value = new_value;
}

CL_Object* cl_add(CL_FUNC_PARAMS) {
    if (count == 0) {
        return cl_make_int(0);
    }

    if (count == 1) {
        CL_Object* operand = args[0];
        CL_CHECK_FUNC_ARG_NUMERIC_TYPE(cl_get_obj_type(operand));
        if (operand == args[0]) {
            cl_inc_refs_cnt(operand);
        }
        return operand;
    }

    CL_Object* result = cl_make_int(0);

    for (size_t i = 0; i < count; i++) {
        CL_Object* operand = args[i];
        CL_CHECK_FUNC_ARG_NUMERIC_TYPE(cl_get_obj_type(operand));

        enum CL_ObjectType operand_type = cl_get_obj_type(operand);
        enum CL_ObjectType result_type = cl_get_obj_type(result);

        if (operand_type == DOUBLE && result_type == INTEGER) {
            double prev_value = cl_get_int_value(result);
            cl_dec_refs_cnt(result);
            result = cl_make_double(prev_value);
            result_type = cl_get_obj_type(result);
        }

        double op_value = operand_type == INTEGER
                         ? cl_get_int_value(operand)
                         : cl_get_double_value(operand);

        if (result_type == DOUBLE) {
            set_double_value(result, cl_get_double_value(result) + op_value);
        } else {
            set_int_value(result, cl_get_int_value(result) + (int)op_value);
        }
    }

    return result;
}

CL_Object* cl_mul(CL_FUNC_PARAMS) {
    if (count == 0) {
        return cl_make_int(1);
    }

    if (count == 1) {
        CL_Object* operand = args[0];
        CL_CHECK_FUNC_ARG_NUMERIC_TYPE(cl_get_obj_type(operand));
        if (operand == args[0]) {
            cl_inc_refs_cnt(operand);
        }
        return operand;
    }

    CL_Object* result = cl_make_int(1);

    for (size_t i = 0; i < count; i++) {
        CL_Object* operand = args[i];
        CL_CHECK_FUNC_ARG_NUMERIC_TYPE(cl_get_obj_type(operand));

        enum CL_ObjectType operand_type = cl_get_obj_type(operand);
        enum CL_ObjectType result_type = cl_get_obj_type(result);

        if (cl_unwrap_numeric_to_double(operand) == 0) {
            cl_dec_refs_cnt(result);
            return cl_make_int(0);
        }

        if (operand_type == DOUBLE && result_type == INTEGER) {
            double prev_value = cl_get_int_value(result);
            cl_dec_refs_cnt(result);
            result = cl_make_double(prev_value);
            result_type = cl_get_obj_type(result);
        }

        double op_value = operand_type == INTEGER
                         ? cl_get_int_value(operand)
                         : cl_get_double_value(operand);

        if (result_type == DOUBLE) {
            set_double_value(result, cl_get_double_value(result) * op_value);
        } else {
            set_int_value(result, cl_get_int_value(result) * (int)op_value);
        }
    }

    return result;
}

CL_Object* cl_div(CL_FUNC_PARAMS) {
    CL_CHECK_FUNC_ARGS_COUNT(count, 0, GREATER);

    if (count == 1) {
        CL_Object* operand = args[0];
        CL_CHECK_FUNC_ARG_NUMERIC_TYPE(cl_get_obj_type(operand));

        if (cl_unwrap_numeric_to_double(operand) == 0) {
            cl_abort("Dividing by zero!\n");
        }

        enum CL_ObjectType type = cl_get_obj_type(operand);

        // 1 / (+-1) = +- 1
        if (type == DOUBLE) {
            double double_value = cl_get_double_value(operand);
            if (double_value == 1 || double_value == -1) {
                if (operand == args[0]) {
                    cl_inc_refs_cnt(operand);
                }
                return operand;
            }
        }

        if (type == INTEGER) {
            double int_value = cl_get_int_value(operand);
            if (int_value == 1 || int_value == -1) {
                if (operand == args[0]) {
                    cl_inc_refs_cnt(operand);
                }
                return operand;
            }
        }

        CL_Object* result = cl_make_double(1 / cl_unwrap_numeric_to_double(operand));
        return result;
    }

    CL_Object* operand1 = args[0];
    CL_Object* operand2 = args[1];
    CL_CHECK_FUNC_ARG_NUMERIC_TYPE(cl_get_obj_type(operand1));
    CL_CHECK_FUNC_ARG_NUMERIC_TYPE(cl_get_obj_type(operand2));

    if (cl_unwrap_numeric_to_double(operand2) == 0) {
        cl_abort("Dividing by zero!\n");
    }

    CL_Object* result = NULL;

    if (cl_get_obj_type(operand1) == DOUBLE ||  cl_get_obj_type(operand2) == DOUBLE) {
        result = cl_make_double(cl_unwrap_numeric_to_double(operand1) / cl_unwrap_numeric_to_double(operand2));
    } else {
        if (cl_get_int_value(operand1) % cl_get_int_value(operand2) == 0) {
            result = cl_make_int(cl_get_int_value(operand1) / cl_get_int_value(operand2));
        } else {
            result = cl_make_double(cl_get_int_value(operand1) * 1.0 / cl_get_int_value(operand2));
        }
    }

    return result;
}

CL_Object* cl_sub(CL_FUNC_PARAMS) {
    CL_CHECK_FUNC_ARGS_COUNT(count, 0, GREATER);

    if (count == 1) {
        CL_Object* operand = args[0];
        CL_CHECK_FUNC_ARG_NUMERIC_TYPE(cl_get_obj_type(operand));

        enum CL_ObjectType type = cl_get_obj_type(operand);

        if (type == INTEGER) {
            set_int_value(operand, -1 * cl_get_int_value(operand));
        } else {
            set_double_value(operand, -1 * cl_get_double_value(operand));
        }
        if (operand == args[0]) {
            cl_inc_refs_cnt(operand);
        }
        return operand;
    }

    CL_Object* operand1 = args[0];
    CL_Object* operand2 = args[1];
    CL_CHECK_FUNC_ARG_NUMERIC_TYPE(cl_get_obj_type(operand1));
    CL_CHECK_FUNC_ARG_NUMERIC_TYPE(cl_get_obj_type(operand2));

    CL_Object* result = NULL;

    if (cl_get_obj_type(operand1) == DOUBLE ||  cl_get_obj_type(operand2) == DOUBLE) {
        result = cl_make_double(cl_unwrap_numeric_to_double(operand1) - cl_unwrap_numeric_to_double(operand2));
    } else {
        result = cl_make_int(cl_get_int_value(operand1) - cl_get_int_value(operand2));
    }

    return result;
}
