#include "core.h"

#include "const.h"
#include "evaluable.h"
#include "memory.h"

Object* make_unspecified() {
    Object* obj = allocate_memory(sizeof(Object));
    obj->type = UNSPECIFIED;
    return obj;
}

void destroy_unspecified(Object* obj) {
    free_memory(obj);
}

void destroy(Object* obj) {
    if (!obj) {
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
        case UNSPECIFIED:
            return "UNSPECIFIED";
    }
    return "UNKNOWN";
}

enum ObjectType get_object_type(Object* obj) {
    return obj->type;
}
