#include "core.h"

#include <stdlib.h>

void destroy(Object* obj) {
    if (!obj) {
        return;
    }

    // TODO:
    free(obj->value);
    free(obj);
}