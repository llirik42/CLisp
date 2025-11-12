#include "const.h"

#include <stdlib.h>

Object* make_int(int value) {
    // TODO:
    IntValue* obj_value = malloc(sizeof(IntValue));
    obj_value->value = value;

    Object* obj = malloc(sizeof(Object));
    obj->value = obj_value;

    return obj;
}
