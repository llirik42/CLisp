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
