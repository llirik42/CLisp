#include "arithmetic.h"

#include "const.h"

Object* clisp_add(Object* a1, Object* a2) {
    // TODO:
    IntValue* v1 = a1->value;
    IntValue* v2 = a2->value;
    return make_int(v1->value + v2->value);
}
