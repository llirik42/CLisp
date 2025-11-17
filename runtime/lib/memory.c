#include "memory.h"
#include "utils.h"

#include <stdlib.h>

void* allocate_memory(size_t size) {
    if (!size) {
        print_error_and_exit("Memory allocation: no memory block size!\n", 0);
    }

    void* ptr = malloc(size);

    if (!ptr) {
        print_error_and_exit("malloc", 1);
    }

    return ptr;
}

void* reallocate_memory(void* ptr, size_t size) {
    if (!size) {
        print_error_and_exit("Memory reallocation: no memory block size!\n", 0);
    }

    void* new_ptr = realloc(ptr, size);

    if (!new_ptr) {
        print_error_and_exit("realloc", 1);
    }

    return new_ptr;
}

void free_memory(void* ptr) {
    if (!ptr) {
        return;
    }

    free(ptr);
}
