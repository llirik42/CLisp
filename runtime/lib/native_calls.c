#include "native_calls.h"
#include <stdio.h>
#include <stdarg.h>

CL_Object* cl_native(const char* func, const char* library, enum CL_NativeType result_type, unsigned int count, ...) {
    // TODO: implement (return lambda)

    printf("%s-%s-%d-%d\n", func, library, result_type, count);

    va_list args;
    va_start(args, count);

    for (unsigned int i = 0; i < count; i++) {
        enum CL_NativeType type = va_arg(args, enum CL_NativeType);
        printf("%d ", type);
    }
    printf("\n");

    return cl_make_unspecified();
}
