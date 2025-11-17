#include "dynamic_array.h"

#include <math.h>

#include "memory.h"
#include "utils.h"

#define BASIC_DA_CAPACITY 10

DynamicArray* da_create() {
    DynamicArray *da = allocate_memory(sizeof(DynamicArray));
    da->capacity = BASIC_DA_CAPACITY;
    da->size = 0;
    da->data = allocate_memory(sizeof(void*) * da->capacity);
    return da;
}

void da_push_back(DynamicArray *da, void *element) {
    if (da->size >= da->capacity) {
        da->capacity = (int)ceil((double)da->capacity * 1.5);
        da->data = reallocate_memory(da->data, sizeof(void*) * da->capacity);
    }

    da->data[da->size++] = element;
}

void* da_get(DynamicArray *da, size_t index) {
    if (index >= da->size) {
        print_error_and_exit("Index out of dynamic array size", 0);
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
