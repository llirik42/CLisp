#pragma once

#include "const_types.h"

enum ObjectType {
    INTEGER,
    DOUBLE,
    RATIO,
    BOOLEAN,
    EVALUABLE,
    STRING,
};

char* get_object_type_name(enum ObjectType type);

typedef struct {
    void* value;
    enum ObjectType type;
} Object;

void destroy(Object* obj);
