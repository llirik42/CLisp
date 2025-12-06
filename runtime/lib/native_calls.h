#pragma once
#include "core.h"

enum CL_NativeType {
    CL_NATIVE_INTEGER,
    CL_NATIVE_DOUBLE,
    CL_NATIVE_CHAR,
    CL_NATIVE_STRING,
    CL_NATIVE_VOID,
};

CL_Object* cl_native(const char* func, const char* library, enum CL_NativeType result_type, unsigned int count, ...);
