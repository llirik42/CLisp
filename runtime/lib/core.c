#include "core.h"

#include "primitive.h"
#include "evaluable.h"
#include "memory.h"

Object* clisp_make_unspecified() {
    Object* obj = allocate_memory(sizeof(Object));
    init_object(obj, UNSPECIFIED);
    return obj;
}

void init_object(Object* obj, enum ObjectType type) {
    obj->type = type;
    obj->ref_count = 1;
}

void increase_refs_count(Object* obj) {
    obj->ref_count++;
}

static void destroy_unspecified(Object* obj) {
    free_memory(obj);
}

void clisp_destroy_object(Object* obj) {
    if (!obj || !obj->ref_count) {
        return;
    }

    if (--obj->ref_count > 0) {
        return;
    }

    switch (get_object_type(obj)) {
        case INTEGER:
            destroy_int(obj);
            break;
        case DOUBLE:
            destroy_double(obj);
            break;
        case BOOLEAN:
            destroy_boolean(obj);
            break;
        case STRING:
            destroy_string(obj);
            break;
        case CHAR:
            destroy_char(obj);
            break;
        case EVALUABLE:
            destroy_evaluable(obj);
            break;
        case UNSPECIFIED:
            destroy_unspecified(obj);
        default: ;
    }
}

char* get_object_type_name(enum ObjectType type) {
    switch(type) {
        case INTEGER:
            return "INTEGER";
        case DOUBLE:
            return "DOUBLE";
        case BOOLEAN:
            return "BOOLEAN";
        case EVALUABLE:
            return "EVALUABLE";
        case STRING:
            return "STRING";
        case CHAR:
            return "CHAR";
        case UNSPECIFIED:
            return "UNSPECIFIED";
    }
    return "UNKNOWN";
}

enum ObjectType get_object_type(Object* obj) {
    return obj->type;
}

unsigned char is_numeric(enum ObjectType type) {
    return type == INTEGER || type == DOUBLE;
}
