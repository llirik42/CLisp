#pragma once

#include "const_types.h"

enum ObjectType {
    INTEGER,
    DOUBLE,
    BOOLEAN,
    EVALUABLE,
    STRING,
    UNSPECIFIED,
};

char* get_object_type_name(enum ObjectType type);

typedef struct {
    void* value;
    enum ObjectType type;
} Object;

#define CLISP_FUNC_PARAMS unsigned int count, Object** args

enum ObjectType get_object_type(Object* obj);

Object* make_unspecified();

void destroy(Object* obj);
