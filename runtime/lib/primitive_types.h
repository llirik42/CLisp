#pragma once

#include "core.h"

typedef struct {
    enum ObjectType type;
    unsigned short ref_count;
    int value;
} IntObject;

typedef struct {
    enum ObjectType type;
    unsigned short ref_count;
    double value;
} DoubleObject;

typedef struct {
    enum ObjectType type;
    unsigned short ref_count;
    unsigned char value;
} BooleanObject;

typedef struct {
    enum ObjectType type;
    unsigned short ref_count;
    char* value;
    unsigned int length;
} StringObject;

typedef struct {
    enum ObjectType type;
    unsigned short ref_count;
    char value;
} CharObject;
