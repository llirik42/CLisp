#include "primitive.h"

#include <ctype.h>
#include <errno.h>
#include <limits.h>
#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "memory.h"
#include "utils.h"
#include "primitive_types.h"

#define TOO_LOW_DOUBLE 1e-308
static void destroy_simple_object(CL_Object* obj) {
    cl_free_memory(obj);
}

CL_Object* cl_make_int(int value) {
    CL_IntObject* int_object = cl_allocate_memory(sizeof(CL_IntObject));
    cl_init_obj((CL_Object*)int_object, INTEGER);
    int_object->value = value;

    return (CL_Object*)int_object;
}

int cl_get_int_value(CL_Object* obj) {
    CL_IntObject* int_object = (CL_IntObject*)obj;
    return int_object->value;
}

void cl_destroy_int(CL_Object* obj) {
    destroy_simple_object(obj);
}

CL_Object* cl_make_double(double value) {
    CL_DoubleObject* double_object = cl_allocate_memory(sizeof(CL_DoubleObject));
    cl_init_obj((CL_Object*)double_object, DOUBLE);
    double_object->value = value;

    return (CL_Object*)double_object;
}

double cl_get_double_value(CL_Object* obj) {
    CL_DoubleObject* double_object = (CL_DoubleObject*)obj;
    return double_object->value;
}

void cl_destroy_double(CL_Object* obj) {
    destroy_simple_object(obj);
}

CL_Object* cl_make_boolean(unsigned char value) {
    if (value != 0 && value != 1) {
        cl_abort("Boolean value must be 0 or 1!\n");
    }

    CL_BooleanObject* boolean_object = cl_allocate_memory(sizeof(CL_BooleanObject));
    cl_init_obj((CL_Object*)boolean_object, BOOLEAN);
    boolean_object->value = value;

    return (CL_Object*)boolean_object;
}

CL_Object* cl_make_true() {
    return cl_make_boolean(1);
}

CL_Object* cl_make_false() {
    return cl_make_boolean(0);
}

unsigned char cl_get_boolean_value(CL_Object* obj) {
    CL_BooleanObject* boolean_object = (CL_BooleanObject*)obj;
    return boolean_object->value;
}

void cl_destroy_boolean(CL_Object* obj) {
    destroy_simple_object(obj);
}

CL_Object* cl_make_string(char* value) {
    CL_StringObject* string_object = cl_allocate_memory(sizeof(CL_StringObject));
    cl_init_obj((CL_Object*)string_object, STRING);
    string_object->length = strlen(value);

    char* container = cl_allocate_memory(sizeof(char) * (string_object->length + 1));
    strcpy(container, value);
    string_object->value = container;

    return (CL_Object*)string_object;
}

char* cl_get_string_value(CL_Object* obj) {
    CL_StringObject* string_object = (CL_StringObject*)obj;
    return string_object->value;
}

unsigned int cl_get_string_length(CL_Object* obj) {
    CL_StringObject* string_object = (CL_StringObject*)obj;
    return string_object->length;
}

void cl_destroy_string(CL_Object* obj) {
    char* container = cl_get_string_value(obj);
    cl_free_memory(container);
    destroy_simple_object(obj);
}

CL_Object* cl_make_char(char value) {
    CL_CharObject* char_object = cl_allocate_memory(sizeof(CL_CharObject));
    cl_init_obj((CL_Object*)char_object, CHAR);
    char_object->value = value;

    return (CL_Object*)char_object;
}

char cl_get_char_value(CL_Object* obj) {
    CL_CharObject* char_object = (CL_CharObject*)obj;
    return char_object->value;
}

void cl_destroy_char(CL_Object* obj) {
    destroy_simple_object(obj);
}

CL_Object* cl_to_integer(CL_FUNC_PARAMS) {
    CL_CHECK_FUNC_ARGS_COUNT(count, 1, EQUAL);
    CL_Object* obj = args[0];

    switch (cl_get_obj_type(obj)) {
        case INTEGER:
            return cl_make_int(cl_get_int_value(obj));
        case DOUBLE:
            return cl_make_int((int)cl_get_double_value(obj));
        case BOOLEAN:
            return cl_make_int(cl_get_boolean_value(obj));
        case CHAR:
            return cl_make_int(cl_get_char_value(obj));
        case STRING: {
            char *end_ptr;
            char* str = cl_get_string_value(obj);
            if (!str || *str == '\0') {
                cl_abort("Cast to integer from string: value must be a non-empty string!\n");
            }

            errno = 0;
            long val = strtol(str, &end_ptr, 10);
            if (errno == ERANGE || val > INT_MAX || val < INT_MIN) {
                cl_abort("Cast to integer from string: number not in integer range!\n");
            }

            if (*end_ptr != '\0') {
                while (isspace((unsigned char)*end_ptr)) {
                    end_ptr++;
                }

                if (*end_ptr != '\0') {
                    cl_abort("Cast to integer from string: inadmissible symbols in string!\n");
                }
            }
            return cl_make_int((int)val);
        }
        default:
            cl_abort("Cast to integer: unexpected type!\n");
            __builtin_unreachable();
    }
}

CL_Object* cl_to_double(CL_FUNC_PARAMS) {
    CL_CHECK_FUNC_ARGS_COUNT(count, 1, EQUAL);
    CL_Object* obj = args[0];

    switch (cl_get_obj_type(obj)) {
        case INTEGER:
            return cl_make_double(cl_get_int_value(obj));
        case DOUBLE:
            return cl_make_double(cl_get_double_value(obj));
        case BOOLEAN:
            return cl_make_double(cl_get_boolean_value(obj));
        case CHAR:
            return cl_make_double(cl_get_char_value(obj));
        case STRING: {
            char *end_ptr;
            char* str = cl_get_string_value(obj);
            if (!str || *str == '\0') {
                cl_abort("Cast to double from string: value must be a non-empty string!\n");
            }

            errno = 0;
            double val = strtod(str, &end_ptr);
            if (errno == ERANGE) {
                if (val == HUGE_VAL || val == -HUGE_VAL) {
                    cl_abort("Cast to double from string: number not in double range!\n");
                }
                if (fabs(val) < TOO_LOW_DOUBLE) {
                    cl_abort("Cast to double from string: number too low!\n");
                }
            }


            if (*end_ptr != '\0') {
                while (isspace((unsigned char)*end_ptr)) {
                    end_ptr++;
                }

                if (*end_ptr != '\0') {
                    const char *suffix = end_ptr;

                    if (strcasecmp(suffix, "inf") == 0 || strcasecmp(suffix, "infinity") == 0 || strcasecmp(suffix, "nan") == 0) {
                        return cl_make_double(val);
                    }

                    if (tolower((unsigned char)*suffix) == 'e') {
                        suffix++;
                        if (*suffix == '+' || *suffix == '-') {
                            suffix++;
                        }
                        while (isdigit((unsigned char)*suffix)) {
                            suffix++;
                        }
                        if (*suffix == '\0') {
                            return cl_make_double(val);
                        }
                    }

                    cl_abort("Cast to double from string: inadmissible symbols in string!\n");
                }
            }

            return cl_make_int((int)val);
        }
        default:
            cl_abort("Cast to double: unexpected type!\n");
            __builtin_unreachable();
    }
}

CL_Object* cl_to_char(CL_FUNC_PARAMS) {
    CL_CHECK_FUNC_ARGS_COUNT(count, 1, EQUAL);
    CL_Object* obj = args[0];

    switch (cl_get_obj_type(obj)) {
        case INTEGER: {
            int val = cl_get_int_value(obj);
            if (val > CHAR_MAX || val < CHAR_MIN) {
                char error[CL_ERROR_BUF_SIZE];
                snprintf(error, sizeof(error), "Cast to char from integer: value must be in range (%d, %d)!\n", CHAR_MIN, CHAR_MAX);
                cl_abort(error);
            }
            return cl_make_char((char)val);
        }
        case BOOLEAN: {
            unsigned char val = cl_get_boolean_value(obj);
            if (val == TRUE) {
                return cl_make_char('t');
            }
            return cl_make_char('f');
        }
        case CHAR:
            return cl_make_char(cl_get_char_value(obj));
        case STRING: {
            char* str = cl_get_string_value(obj);
            if (strlen(str) != 0) {
                cl_abort("Cast to char from string: length of string not equal 1!\n");
            }
            return cl_make_char(*str);
        }
        default:
            cl_abort("Cast to char: unexpected type!\n");
            __builtin_unreachable();
    }
}

CL_Object* cl_to_string(CL_FUNC_PARAMS) {
    CL_CHECK_FUNC_ARGS_COUNT(count, 1, EQUAL);
    CL_Object* obj = args[0];

    switch (cl_get_obj_type(obj)) {
        case INTEGER: {
            int val = cl_get_int_value(obj);
            // INT_MIN = -2147483648 (11 symbols) + \0
            char* buffer = cl_allocate_memory(12 * sizeof(char));
            sprintf(buffer, "%d", val);
            return cl_make_string(buffer);
        }
        case DOUBLE: {
            double val = cl_get_double_value(obj);
            // DOUBLE can contain 308 digits in integer part + decimal part + \0
            char* buffer = cl_allocate_memory(350 * sizeof(char));
            sprintf(buffer, "%g", val);
            buffer = cl_reallocate_memory(buffer, strlen(buffer) + 1);
            return cl_make_string(buffer);
        }
        case BOOLEAN: {
            unsigned char val = cl_get_boolean_value(obj);
            if (val == TRUE) {
                return cl_make_string("true");
            }
            return cl_make_string("false");
        }
        case CHAR: {
            char buff[2];
            buff[0] = cl_get_char_value(obj);;
            buff[1] = '\0';
            return cl_make_string(buff);
        }
        case STRING:
            return cl_make_string(cl_get_string_value(obj));
        default:
            cl_abort("Cast to string: unexpected type!\n");
            __builtin_unreachable();
    }
}

CL_Object* cl_to_boolean(CL_FUNC_PARAMS) {
    CL_CHECK_FUNC_ARGS_COUNT(count, 1, EQUAL);
    CL_Object* obj = args[0];

    switch (cl_get_obj_type(obj)) {
        case INTEGER: {
            int val = cl_get_int_value(obj);
            switch (val) {
                case TRUE:
                    return cl_make_true();
                case FALSE:
                    return cl_make_false();
                default:
                    cl_abort("Cast to boolean from int: value not equal 0 or 1!\n");
                    __builtin_unreachable();
            }
        }
        case BOOLEAN:
            return cl_make_boolean(cl_get_boolean_value(obj));
        case CHAR: {
            char val = cl_get_char_value(obj);
            switch (val) {
                case 't':
                    return cl_make_true();
                case 'f':
                    return cl_make_false();
                default:
                    cl_abort("Cast to boolean from char: value not equal 't' or 'f'!\n");
                    __builtin_unreachable();
            }
        }
        case STRING: {
            char* val = cl_get_string_value(obj);
            if (!strcmp(val, "true")) {
                return cl_make_true();
            }
            if (!strcmp(val, "false")) {
                return cl_make_false();
            }
            cl_abort("Cast to boolean from string: value not equal 'true' or 'false'!\n");
            __builtin_unreachable();
        }
        default:
            cl_abort("Cast to boolean: unexpected type!\n");
            __builtin_unreachable();
    }
}
