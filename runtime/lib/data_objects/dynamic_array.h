#pragma once
#include <stddef.h>

typedef struct {
    void **data;
    size_t size;
    size_t capacity;
} DynamicArray;

DynamicArray* da_create(unsigned short capacity);

void da_append(DynamicArray *da, void *element);

void da_pop(DynamicArray *da);

void* da_get(DynamicArray *da, size_t index);

void da_destroy(DynamicArray *da);

size_t da_size(DynamicArray *da);
