#pragma once

enum ObjectType {
    INTEGER,
    DOUBLE,
    RATIO
};

typedef struct {
    void* value;
    enum ObjectType type;
} Object;

typedef struct {
    int value;
} IntValue;

void destroy(Object* obj);
