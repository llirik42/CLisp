#include "runtime.h"
#include "malloc.h"
#include "stdio.h"

typedef struct {
    int value;
} IntValue;

Object* make_int(int value) {
    // TODO:
    IntValue* obj_value = malloc(sizeof(IntValue));
    obj_value->value = value;

    Object* obj = malloc(sizeof(Object));
    obj->value = obj_value;

    return obj;
}

void destroy(Object* obj) {
    if (!obj) {
        return;
    }

    // TODO:
    free(obj->value);
    free(obj);
}

Object* clisp_display(Object* obj) {
    // TODO:
    IntValue* v = obj->value;
    printf("%d\n", v->value);
    return NULL;
}

Object* clisp_add(Object* a1, Object* a2) {
    // TODO:
    IntValue* v1 = a1->value;
    IntValue* v2 = a2->value;
    return make_int(v1->value + v2->value);
}
