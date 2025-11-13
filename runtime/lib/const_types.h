#pragma once

typedef struct {
    int value;
} IntValue;

typedef struct {
    double value;
} DoubleValue;

typedef struct {
    unsigned char value;
} BooleanValue;

typedef struct {
    char* value;
    unsigned int length;
} StringValue;
