#pragma once
#include "core.h"

enum CL_NativeType {
    CL_NATIVE_INTEGER,
    CL_NATIVE_DOUBLE,
    CL_NATIVE_CHAR,
    CL_NATIVE_STRING,
    CL_NATIVE_VOID,
};

typedef struct {
    enum CL_NativeType type;
    CL_Object* value;
} CL_NativeArgument;

CL_Object* cl_native(char* func, char* library, enum CL_NativeType result_type, unsigned int count, CL_NativeArgument* args);
