#include "dynamic_array.h"

#include <math.h>
#include <stdio.h>

#include "memory.h"
#include "utils.h"

#define BASIC_DA_CAPACITY 10
#define CAPACITY_MULTIPLIER 1.5

CL_DynamicArray* cl_da_create(unsigned short capacity) {
    CL_DynamicArray *da = cl_allocate_memory(sizeof(CL_DynamicArray));
    if (!capacity) {
        da->capacity = BASIC_DA_CAPACITY;
    } else {
        da->capacity = capacity;
    }
    da->size = 0;
    da->data = cl_allocate_memory(sizeof(void*) * da->capacity);
    return da;
}

void cl_da_append(CL_DynamicArray *da, void *element) {
    if (da->size >= da->capacity) {
        da->capacity = (int)ceil((double)da->capacity * CAPACITY_MULTIPLIER);
        da->data = cl_reallocate_memory(da->data, sizeof(void*) * da->capacity);
    }

    da->data[da->size++] = element;
}

void cl_da_pop(CL_DynamicArray *da) {
    if (da->size <= 0) {
        cl_abort("Dynamic Array underflow\n");
        __builtin_unreachable();
    }

    da->size--;
}

void* cl_da_get(CL_DynamicArray *da, size_t index) {
    if (index >= da->size) {
        cl_abort("Index out of dynamic array size");
    }

    return da->data[index];
}

void cl_da_destroy(CL_DynamicArray *da) {
    cl_free_memory(da->data);
    cl_free_memory(da);
}

size_t cl_da_size(CL_DynamicArray *da) {
    return da->size;
}
