#include "native_calls.h"
#include <stdio.h>

CL_Object* cl_native(char* func, char* library, enum CL_NativeType result_type, unsigned int count, enum CL_NativeType* args_types) {
    // TODO: implement (return lambda)
    printf("%s-%s-%d-%d-%p\n", func, library, result_type, count, (void*)args_types);
    return cl_make_unspecified();
}
