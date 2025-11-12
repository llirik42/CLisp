#pragma once

#include "const_types.h"

enum ObjectType {
    INTEGER,
    DOUBLE,
    RATIO,
    POSTPONED,
};

typedef struct {
    void* value;
    enum ObjectType type;
} Object;

void destroy(Object* obj);
