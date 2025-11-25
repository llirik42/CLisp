#include "memory.h"
#include "utils.h"

#include <stdlib.h>

void* allocate_memory(size_t size) {
    if (!size) {
        clisp_exit("Memory allocation: no memory block size!\n");
    }

    void* ptr = malloc(size);

    if (!ptr) {
        clisp_exit_errno("malloc");
    }

    return ptr;
}

void* reallocate_memory(void* ptr, size_t size) {
    if (!size) {
        clisp_exit("Memory reallocation: no memory block size!\n");
    }

    void* new_ptr = realloc(ptr, size);

    if (!new_ptr) {
        clisp_exit_errno("realloc");
    }

    return new_ptr;
}

void free_memory(void* ptr) {
    if (!ptr) {
        return;
    }

    free(ptr);
}
