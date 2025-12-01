#pragma once
#include <stddef.h>

typedef struct {
    void **data;
    size_t size;
    size_t capacity;
} CL_DynamicArray;

#define UNDEFINED_DA_CAPACITY 0

CL_DynamicArray* cl_da_create(unsigned short capacity);

void cl_da_append(CL_DynamicArray *da, void *element);

void cl_da_pop(CL_DynamicArray *da);

void* cl_da_get(CL_DynamicArray *da, size_t index);

void cl_da_destroy(CL_DynamicArray *da);

size_t cl_da_size(CL_DynamicArray *da);
