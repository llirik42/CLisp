#include "const.h"

#include "memory.h"
#include "utils.h"

Object* make_int(int value) {
    IntValue* obj_value = allocate_memory(sizeof(IntValue));
    obj_value->value = value;

    Object* obj = allocate_memory(sizeof(Object));
    obj->value = obj_value;
    obj->type = INTEGER;

    return obj;
}

Object* make_double(double value) {
    DoubleValue* obj_value = allocate_memory(sizeof(IntValue));
    obj_value->value = value;

    Object* obj = allocate_memory(sizeof(Object));
    obj->value = obj_value;
    obj->type = DOUBLE;

    return obj;
}

Object* make_boolean(unsigned char value) {

    if (value != 0 && value != 1) {
        print_error_and_exit("Boolean value must be 0 or 1!\n", 0);
    }

    BooleanValue* obj_value = allocate_memory(sizeof(BooleanValue));
    obj_value->value = value;

    Object* obj = allocate_memory(sizeof(Object));
    obj->value = obj_value;
    obj->type = BOOLEAN;

    return obj;
}

Object* make_string(char* value) {
    StringValue* obj_value = allocate_memory(sizeof(StringValue));
    obj_value->value = value;

    Object* obj = allocate_memory(sizeof(Object));
    obj->value = obj_value;
    obj->type = STRING;

    return obj;
}
