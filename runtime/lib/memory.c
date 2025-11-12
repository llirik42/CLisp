#include "memory.h"

#include <stdio.h>
#include <stdlib.h>

void check_allocated(void* ptr) {
    if (!ptr) {
        perror("Not enough memory!");
        exit(EXIT_FAILURE);
    }
}

void* allocate_memory(size_t size) {
    if (!size) {
        perror("Memory allocation: no memory block size!");
        exit(EXIT_FAILURE);
    }

    void* ptr = malloc(size);
    check_allocated(ptr);
    return ptr;
}

void free_memory(void* ptr) {
    if (!ptr) {
        return;
    }

    free(ptr);
}
