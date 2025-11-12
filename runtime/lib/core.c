#include "core.h"

#include "memory.h"

void destroy(Object* obj) {
    if (!obj) {
        return;
    }

    // TODO:
    free_memory(obj->value);
    free_memory(obj);
}


char* get_object_type_name(enum ObjectType type) {
    switch(type) {
        case INTEGER:
            return "INTEGER";
        case DOUBLE:
            return "DOUBLE";
        case RATIO:
            return "RATIO";
        case BOOLEAN:
            return "BOOLEAN";
        case EVALUABLE:
            return "EVALUABLE";
        case STRING:
            return "STRING";
    }
    return "UNKNOWN";
}
