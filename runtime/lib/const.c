#include "const.h"

#include <string.h>

#include "memory.h"
#include "utils.h"
#include "const_types.h"

static void destroy_simple_object(Object* obj) {
    free_memory(obj);
}

Object* make_int(int value) {
    IntObject* obj_value = allocate_memory(sizeof(IntObject));
    obj_value->value = value;
    obj_value->type = INTEGER;

    return (Object*)obj_value;
}

int get_int_value(Object* obj) {
    IntObject* obj_value = (IntObject*)obj;
    return obj_value->value;
}

void destroy_int(Object* obj) {
    destroy_simple_object(obj);
}

Object* make_double(double value) {
    DoubleObject* obj_value = allocate_memory(sizeof(DoubleObject));
    obj_value->value = value;
    obj_value->type = DOUBLE;

    return (Object*)obj_value;
}

double get_double_value(Object* obj) {
    DoubleObject* obj_value = (DoubleObject*)obj;
    return obj_value->value;
}

void destroy_double(Object* obj) {
    destroy_simple_object(obj);
}

Object* make_boolean(unsigned char value) {
    if (value != 0 && value != 1) {
        print_error_and_exit("Boolean value must be 0 or 1!\n", 0);
    }

    BooleanObject* obj_value = allocate_memory(sizeof(BooleanObject));
    obj_value->value = value;
    obj_value->type = BOOLEAN;

    return (Object*)obj_value;
}

Object* make_true() {
    return make_boolean(1);
}

Object* make_false() {
    return make_boolean(0);
}

unsigned char get_boolean_value(Object* obj) {
    BooleanObject* obj_value = (BooleanObject*)obj;
    return obj_value->value;
}

void destroy_boolean(Object* obj) {
    destroy_simple_object(obj);
}

Object* make_string(char* value) {
    StringObject* obj_value = allocate_memory(sizeof(StringObject));
    obj_value->length = strlen(value);

    char* container = allocate_memory(sizeof(char) * (obj_value->length + 1));
    strcpy(container, value);
    obj_value->value = container;
    obj_value->type = STRING;

    return (Object*)obj_value;
}

char* get_string_value(Object* obj) {
    StringObject* obj_value = (StringObject*)obj;
    return obj_value->value;
}

unsigned int get_string_length(Object* obj) {
    StringObject* obj_value = (StringObject*)obj;
    return obj_value->length;
}

void destroy_string(Object* obj) {
    char* container = get_string_value(obj);
    free_memory(container);
    destroy_simple_object(obj);
}

Object* make_char(char value) {
    CharObject* obj_value = allocate_memory(sizeof(CharObject));
    obj_value->value = value;
    obj_value->type = CHAR;

    return (Object*)obj_value;
}

char get_char_value(Object* obj) {
    CharObject* obj_value = (CharObject*)obj;
    return obj_value->value;
}

void destroy_char(Object* obj) {
    destroy_simple_object(obj);
}
