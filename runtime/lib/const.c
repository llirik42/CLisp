#include "const.h"

#include "memory.h"

Object* make_int(int value) {
    // TODO:
    IntValue* obj_value = allocate_memory(sizeof(IntValue));
    obj_value->value = value;

    Object* obj = allocate_memory(sizeof(Object));
    obj->value = obj_value;

    return obj;
}
