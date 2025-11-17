#include "memory.h"

#include <stdio.h>
#include <stdlib.h>

#include "utils.h"

static void check_allocated(void* ptr) {
    if (!ptr) {
        print_error_and_exit("malloc", 1);
    }
}

void* allocate_memory(size_t size) {
    if (!size) {
        print_error_and_exit("Memory allocation: no memory block size!\n", 0);
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
