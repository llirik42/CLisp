#include "native_calls.h"
#include <stdio.h>

CL_Object* cl_native(char* func, char* library, enum CL_NativeType result_type, unsigned int count, CL_NativeArgument* args) {
    // TODO: implement
    printf("%s-%s-%d-%d-%p\n", func, library, result_type, count, (void*)args);
    return cl_make_unspecified();
}
