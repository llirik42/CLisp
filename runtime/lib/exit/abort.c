#include "abort.h"

#include <stdio.h>
#include <stdlib.h>

void cl_abort(char* message) {
    fprintf(stderr, "%s", message);
    abort();
}

void cl_abort_errno(char* message) {
    perror(message);
    abort();
}
