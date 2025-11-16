#pragma once

#include "core.h"

typedef struct {
    enum ObjectType type;
    int value;
} IntValue;

typedef struct {
    enum ObjectType type;
    double value;
} DoubleValue;

typedef struct {
    enum ObjectType type;
    unsigned char value;
} BooleanValue;

typedef struct {
    enum ObjectType type;
    char* value;
    unsigned int length;
} StringValue;

typedef struct {
    enum ObjectType type;
    char value;
} CharValue;
