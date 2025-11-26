#include "dynamic_array.h"

#include <math.h>
#include <stdio.h>

#include "memory.h"
#include "utils.h"

#define BASIC_DA_CAPACITY 10
#define CAPACITY_MULTIPLIER 1.5

DynamicArray* da_create(unsigned short capacity) {
    DynamicArray *da = allocate_memory(sizeof(DynamicArray));
    if (!capacity) {
        da->capacity = BASIC_DA_CAPACITY;
    } else {
        da->capacity = capacity;
    }
    da->size = 0;
    da->data = allocate_memory(sizeof(void*) * da->capacity);
    return da;
}

void da_append(DynamicArray *da, void *element) {
    if (da->size >= da->capacity) {
        da->capacity = (int)ceil((double)da->capacity * CAPACITY_MULTIPLIER);
        da->data = reallocate_memory(da->data, sizeof(void*) * da->capacity);
    }

    da->data[da->size++] = element;
}

void da_pop(DynamicArray *da) {
    if (da->size <= 0) {
        clisp_exit("Dynamic Array underflow\n");
        __builtin_unreachable();
    }

    da->size--;
}

void* da_get(DynamicArray *da, size_t index) {
    if (index >= da->size) {
        clisp_exit("Index out of dynamic array size");
    }

    return da->data[index];
}

void da_destroy(DynamicArray *da) {
    free_memory(da->data);
    free_memory(da);
}

size_t da_size(DynamicArray *da) {
    return da->size;
}
