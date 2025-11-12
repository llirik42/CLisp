#include <stdio.h>
#include <stdlib.h>

#include "utils.h"

void check_allocated(void* memory) {
    if (!memory) {
        perror("No enough memory");
        exit(EXIT_FAILURE);
    }
}
