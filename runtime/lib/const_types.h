#pragma once

#include "core.h"

typedef struct {
    enum ObjectType type;
    int value;
} IntObject;

typedef struct {
    enum ObjectType type;
    double value;
} DoubleObject;

typedef struct {
    enum ObjectType type;
    unsigned char value;
} BooleanObject;

typedef struct {
    enum ObjectType type;
    char* value;
    unsigned int length;
} StringObject;

typedef struct {
    enum ObjectType type;
    char value;
} CharObject;
