#include "runtime.h"
#include "malloc.h"
#include "stdio.h"

typedef struct {
    int value;
} IntValue;

Object* make_int(int value) {
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

    free(obj->value);
    free(obj);
}

void print(Object* obj) {
    IntValue* v = obj->value;
    printf("%d\n", v->value);
}
