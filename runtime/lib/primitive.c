#include "primitive.h"

#include <string.h>

#include "memory.h"
#include "utils.h"
#include "primitive_types.h"

static void destroy_simple_object(Object* obj) {
    free_memory(obj);
}

Object* make_int(int value) {
    IntObject* int_object = allocate_memory(sizeof(IntObject));
    init_object((Object*)int_object, INTEGER);
    int_object->value = value;

    return (Object*)int_object;
}

int get_int_value(Object* obj) {
    IntObject* int_object = (IntObject*)obj;
    return int_object->value;
}

void destroy_int(Object* obj) {
    destroy_simple_object(obj);
}

Object* make_double(double value) {
    DoubleObject* double_object = allocate_memory(sizeof(DoubleObject));
    init_object((Object*)double_object, DOUBLE);
    double_object->value = value;

    return (Object*)double_object;
}

double get_double_value(Object* obj) {
    DoubleObject* double_object = (DoubleObject*)obj;
    return double_object->value;
}

void destroy_double(Object* obj) {
    destroy_simple_object(obj);
}

Object* make_boolean(unsigned char value) {
    if (value != 0 && value != 1) {
        print_error_and_exit("Boolean value must be 0 or 1!\n", 0);
    }

    BooleanObject* boolean_object = allocate_memory(sizeof(BooleanObject));
    init_object((Object*)boolean_object, BOOLEAN);
    boolean_object->value = value;

    return (Object*)boolean_object;
}

Object* make_true() {
    return make_boolean(1);
}

Object* make_false() {
    return make_boolean(0);
}

unsigned char get_boolean_value(Object* obj) {
    BooleanObject* boolean_object = (BooleanObject*)obj;
    return boolean_object->value;
}

void destroy_boolean(Object* obj) {
    destroy_simple_object(obj);
}

Object* make_string(char* value) {
    StringObject* string_object = allocate_memory(sizeof(StringObject));
    init_object((Object*)string_object, STRING);
    string_object->length = strlen(value);

    char* container = allocate_memory(sizeof(char) * (string_object->length + 1));
    strcpy(container, value);
    string_object->value = container;

    return (Object*)string_object;
}

char* get_string_value(Object* obj) {
    StringObject* string_object = (StringObject*)obj;
    return string_object->value;
}

unsigned int get_string_length(Object* obj) {
    StringObject* string_object = (StringObject*)obj;
    return string_object->length;
}

void destroy_string(Object* obj) {
    char* container = get_string_value(obj);
    free_memory(container);
    destroy_simple_object(obj);
}

Object* make_char(char value) {
    CharObject* char_object = allocate_memory(sizeof(CharObject));
    init_object((Object*)char_object, CHAR);
    char_object->value = value;

    return (Object*)char_object;
}

char get_char_value(Object* obj) {
    CharObject* char_object = (CharObject*)obj;
    return char_object->value;
}

void destroy_char(Object* obj) {
    destroy_simple_object(obj);
}
