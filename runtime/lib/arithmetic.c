#include "arithmetic.h"

#include <stddef.h>

#include "const.h"
#include "evaluable.h"
#include "utils.h"
#include "const_types.h"

static void set_int_value(Object* obj, int new_value) {
    IntObject* obj_value = (IntObject*)obj;
    obj_value->value = new_value;
}

static void set_double_value(Object* obj, double new_value) {
    DoubleObject* obj_value = (DoubleObject*)obj;
    obj_value->value = new_value;
}

Object* clisp_add(CLISP_FUNC_PARAMS) {
    if (count == 0) {
        return make_int(0);
    }

    if (count == 1) {
        Object* operand = unwrap_object(args[0]);
        CHECK_FUNC_ARGUMENT_NUMERIC_TYPE(get_object_type(operand));
        return operand;
    }

    Object* result = make_int(0);

    for (unsigned int i = 0; i < count; i++) {
        Object* operand = unwrap_object(args[i]);
        CHECK_FUNC_ARGUMENT_NUMERIC_TYPE(get_object_type(operand));

        if (get_object_type(operand) == DOUBLE && get_object_type(result) == INTEGER) {
            double prev_value = get_int_value(result);
            destroy(result);
            result = make_double(prev_value);
        }

        double op_value = get_object_type(operand) == INTEGER
                         ? get_int_value(operand)
                         : get_double_value(operand);

        if (get_object_type(result) == DOUBLE) {
            set_double_value(result, get_double_value(result) + op_value);
        } else {
            set_int_value(result, get_int_value(result) + (int)op_value);
        }

        destroy_if_unwrapped(args[i], operand);
    }

    return result;
}

Object* clisp_mul(CLISP_FUNC_PARAMS) {
    if (count == 0) {
        return make_int(1);
    }

    if (count == 1) {
        Object* operand = unwrap_object(args[0]);
        CHECK_FUNC_ARGUMENT_NUMERIC_TYPE(get_object_type(operand));
        return operand;
    }

    Object* result = make_int(1);

    for (unsigned int i = 0; i < count; i++) {
        Object* operand = unwrap_object(args[i]);
        CHECK_FUNC_ARGUMENT_NUMERIC_TYPE(get_object_type(operand));

        if (unwrap_numeric_to_double(operand) == 0) {
            destroy(result);
            destroy_if_unwrapped(args[i], operand);
            return make_int(0);
        }

        if (get_object_type(operand) == DOUBLE && get_object_type(result) == INTEGER) {
            double prev_value = get_int_value(result);
            destroy(result);
            result = make_double(prev_value);
        }

        double op_value = get_object_type(operand) == INTEGER
                         ? get_int_value(operand)
                         : get_double_value(operand);

        if (get_object_type(result) == DOUBLE) {
            set_double_value(result, get_double_value(result) * op_value);
        } else {
            set_int_value(result, get_int_value(result) * (int)op_value);
        }

        destroy_if_unwrapped(args[i], operand);
    }

    return result;
}

Object* clisp_div(CLISP_FUNC_PARAMS) {
    CHECK_FUNC_ARGUMENTS_COUNT(count, 0, GREATER);

    if (count == 1) {
        Object* operand = unwrap_object(args[0]);
        CHECK_FUNC_ARGUMENT_NUMERIC_TYPE(get_object_type(operand));

        if (unwrap_numeric_to_double(operand) == 0) {
            print_error_and_exit("Dividing by zero!\n", 0);
        }

        enum ObjectType type = get_object_type(operand);
        
        // 1 / (+-1) = +- 1
        if ((type == DOUBLE && (get_double_value(operand) == 1 || get_double_value(operand) == -1))
            || (type == INTEGER && (get_int_value(operand) == 1 || get_int_value(operand) == -1))) {
            return operand;
        }

        Object* result = make_double(1 / unwrap_numeric_to_double(operand));
        destroy_if_unwrapped(args[0], operand);
        return result;
    }

    Object* operand1 = unwrap_object(args[0]);
    Object* operand2 = unwrap_object(args[1]);
    CHECK_FUNC_ARGUMENT_NUMERIC_TYPE(get_object_type(operand1));
    CHECK_FUNC_ARGUMENT_NUMERIC_TYPE(get_object_type(operand2));

    if (unwrap_numeric_to_double(operand2) == 0) {
        print_error_and_exit("Dividing by zero!\n", 0);
    }

    Object* result = NULL;

    if (get_object_type(operand1) == DOUBLE ||  get_object_type(operand2) == DOUBLE) {
        result = make_double(unwrap_numeric_to_double(operand1) / unwrap_numeric_to_double(operand2));
    } else {
        if (get_int_value(operand1) % get_int_value(operand2) == 0) {
            result = make_int(get_int_value(operand1) / get_int_value(operand2));
        } else {
            result = make_double(get_int_value(operand1) * 1.0 / get_int_value(operand2));
        }
    }

    destroy_if_unwrapped(args[0], operand1);
    destroy_if_unwrapped(args[1], operand2);

    return result;
}

Object* clisp_sub(CLISP_FUNC_PARAMS) {
    CHECK_FUNC_ARGUMENTS_COUNT(count, 0, GREATER);

    if (count == 1) {
        Object* operand = unwrap_object(args[0]);
        CHECK_FUNC_ARGUMENT_NUMERIC_TYPE(get_object_type(operand));

        enum ObjectType type = get_object_type(operand);

        if (type == INTEGER) {
            set_int_value(operand, -1 * get_int_value(operand));
        } else {
            set_double_value(operand, -1 * get_double_value(operand));
        }
        return operand;
    }

    Object* operand1 = unwrap_object(args[0]);
    Object* operand2 = unwrap_object(args[1]);
    CHECK_FUNC_ARGUMENT_NUMERIC_TYPE(get_object_type(operand1));
    CHECK_FUNC_ARGUMENT_NUMERIC_TYPE(get_object_type(operand2));

    Object* result = NULL;

    if (get_object_type(operand1) == DOUBLE ||  get_object_type(operand2) == DOUBLE) {
        result = make_double(unwrap_numeric_to_double(operand1) - unwrap_numeric_to_double(operand2));
    } else {
        result = make_int(get_int_value(operand1) - get_int_value(operand2));
    }

    destroy_if_unwrapped(args[0], operand1);
    destroy_if_unwrapped(args[1], operand2);

    return result;
}
