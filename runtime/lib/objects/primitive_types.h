#pragma once

#include "lib/core.h"

typedef struct {
    enum CL_ObjectType type;
    unsigned short ref_count;
    int value;
} CL_IntObject;

typedef struct {
    enum CL_ObjectType type;
    unsigned short ref_count;
    double value;
} CL_DoubleObject;

typedef struct {
    enum CL_ObjectType type;
    unsigned short ref_count;
    bool value;
} CL_BooleanObject;

typedef struct {
    enum CL_ObjectType type;
    unsigned short ref_count;
    char* value;
    size_t length;
} CL_StringObject;

typedef struct {
    enum CL_ObjectType type;
    unsigned short ref_count;
    char value;
} CL_CharObject;
