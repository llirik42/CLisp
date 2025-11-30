#include "primitive.h"

#include <string.h>

#include "memory.h"
#include "utils.h"
#include "primitive_types.h"

static void destroy_simple_object(CL_Object* obj) {
    free_memory(obj);
}

CL_Object* cl_make_int(int value) {
    CL_IntObject* int_object = allocate_memory(sizeof(CL_IntObject));
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
    CL_DoubleObject* double_object = allocate_memory(sizeof(CL_DoubleObject));
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

    CL_BooleanObject* boolean_object = allocate_memory(sizeof(CL_BooleanObject));
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
    CL_StringObject* string_object = allocate_memory(sizeof(CL_StringObject));
    cl_init_obj((CL_Object*)string_object, STRING);
    string_object->length = strlen(value);

    char* container = allocate_memory(sizeof(char) * (string_object->length + 1));
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
    free_memory(container);
    destroy_simple_object(obj);
}

CL_Object* cl_make_char(char value) {
    CL_CharObject* char_object = allocate_memory(sizeof(CL_CharObject));
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
