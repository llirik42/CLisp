#include "native_calls.h"
#include <stdio.h>
#include <stdarg.h>
#include <dlfcn.h>
#include <ffi.h>
#include <setjmp.h>
#include <signal.h>
#include <stdlib.h>
#include <string.h>

#include "memory.h"
#include "utils.h"
#include "objects/lambda.h"
#include "objects/primitive.h"

// 8 + 1 NULL
#define DLL_VARIANTS_COUNT_MAX 9

#define HANDLE_OBJ(OBJ_TYPE, NATIVE_TYPE, C_TYPE, GETTER) \
case OBJ_TYPE: { \
if (data->args_types[i] != NATIVE_TYPE) { \
cl_abort("Native call: object type not equal assigned type!\n"); \
} \
C_TYPE val = GETTER(args[i]); \
C_TYPE* ptr = cl_allocate_memory(sizeof(C_TYPE)); \
*ptr = val; \
variables[i] = ptr; \
break; \
}

#define HANDLE_RET_VALUE(NATIVE_TYPE, C_TYPE, CREATOR) \
case NATIVE_TYPE: \
ret_obj = CREATOR(*(C_TYPE*)result); \
break;


static sigjmp_buf segv_jmp_buf;

static void segv_handler(int sig, siginfo_t *info, void *ucontext) {
    (void)sig;
    (void)info;
    (void)ucontext;
    siglongjmp(segv_jmp_buf, 1);
}

typedef struct CLNativeTypeToFFIType {
    enum CL_NativeType cl_native_type;
    ffi_type* ffi_type;
} CLNativeTypeToFFIType;

static const CLNativeTypeToFFIType map_cl_native_type_to_ffi_type[] = {
    {CL_NATIVE_INTEGER, &ffi_type_sint},
    {CL_NATIVE_DOUBLE, &ffi_type_double},
    {CL_NATIVE_CHAR, &ffi_type_schar},
    {CL_NATIVE_STRING, &ffi_type_pointer},
    {CL_NATIVE_VOID, &ffi_type_void},
};

static ffi_type* get_ffi_type(enum CL_NativeType type) {
    for (size_t i = 0; i < sizeof(map_cl_native_type_to_ffi_type) / sizeof(map_cl_native_type_to_ffi_type[0]); i++) {
        if (map_cl_native_type_to_ffi_type[i].cl_native_type == type) {
            return map_cl_native_type_to_ffi_type[i].ffi_type;
        }
    }
    return NULL;
}

typedef struct LibNameToDLL {
    const char* name;
    const char* variants[DLL_VARIANTS_COUNT_MAX];
} LibNameToDLL;

static const LibNameToDLL map_lib_name_type_to_dll[] = {
    {"cmath", {"libm.so.6", "libm.dylib", NULL} },
};

static const char** find_dll_variants(const char* name) {
    for (size_t i = 0; i < sizeof(map_lib_name_type_to_dll) / sizeof(map_lib_name_type_to_dll[0]); i++) {
        if (!strcmp(map_lib_name_type_to_dll[i].name, name)) {
            return (const char**)map_lib_name_type_to_dll[i].variants;
        }
    }
    return NULL;
}

static char* get_function(const char* func_name, const char* libname) {
    void* func_ptr = NULL;

    // Поиск в текущем процессе (включая libc)
    func_ptr = dlsym(RTLD_DEFAULT, func_name);
    if (func_ptr) return func_ptr;

    const char** dll_variants = find_dll_variants(libname);
    if (dll_variants == NULL) {
        cl_abort("Library not found\n");
        __builtin_unreachable();
    }

    unsigned char curr_variant_pos = 0;
    while (dll_variants[curr_variant_pos]) {
        void* dll = dlopen(dll_variants[curr_variant_pos], RTLD_NOW);
        if (dll) {
            void* dll_func_ptr = dlsym(dll, func_name);
            if (dll_func_ptr) {
                return dll_func_ptr;
            }
        }
        curr_variant_pos++;
    }

    cl_abort("Function not found\n");
    __builtin_unreachable();
}

CL_Object* cl_call_native(CL_NativeData* data, CL_FUNC_PARAMS) {
    if (!data) {
        cl_abort("Native call: without data!\n");
        __builtin_unreachable();
    }

    ffi_cif cif;
    ffi_type** arg_types = NULL;
    if (count) {
        arg_types = cl_allocate_memory(sizeof(ffi_type*) * count);
    }

    for (size_t i = 0; i < count; i++) {
        ffi_type* type = get_ffi_type(data->args_types[i]);
        if (!type) {
            cl_abort("Native call: unknown assigned argument type!\n");
            __builtin_unreachable();
        }

        if (arg_types) {
            arg_types[i] = type;
        }
    }

    ffi_status status = ffi_prep_cif(&cif, FFI_DEFAULT_ABI,  count, get_ffi_type(data->return_type), arg_types);
    if (status != FFI_OK) {
        cl_abort("Native call: preparation failed!\n");
        __builtin_unreachable();
    }

    ffi_type* ret_type = get_ffi_type(data->return_type);
    if (!ret_type) {
        cl_abort("Native call: unknown assigned returning type!\n");
        __builtin_unreachable();
    }

    size_t result_size = ret_type->size > sizeof(ffi_arg) ? ret_type->size : sizeof(ffi_arg);

    void* result = NULL;

    if (ret_type != &ffi_type_void) {
        result = cl_allocate_memory(result_size);
        memset(result, 0, result_size);
    }

    void* variables[count];
    for (size_t i = 0; i < count; i++) {
        switch (args[i]->type) {
            HANDLE_OBJ(INTEGER, CL_NATIVE_INTEGER, int, cl_get_int_value)
            HANDLE_OBJ(DOUBLE, CL_NATIVE_DOUBLE, double, cl_get_double_value)
            HANDLE_OBJ(CHAR, CL_NATIVE_CHAR, char, cl_get_char_value)
            HANDLE_OBJ(STRING, CL_NATIVE_STRING, char*, cl_get_string_value)

            case UNSPECIFIED:
                variables[i] = NULL;
                break;
            default:
                cl_abort("Native call: unknown argument type!\n");
        }
    }

    // Intercepting SIGSEGV from ffi_call. It raises when ffi_call failed.
    struct sigaction old_sa;
    struct sigaction sa = {0};

    sa.sa_sigaction = segv_handler;
    sa.sa_flags = SA_SIGINFO;
    sigemptyset(&sa.sa_mask);

    if (sigaction(SIGSEGV, &sa, &old_sa) < 0) {
        cl_abort_errno("sigaction");
    }

    if (sigsetjmp(segv_jmp_buf, 1) == 0) {
        ffi_call(&cif, FFI_FN(data->func), result, variables);
        sigaction(SIGSEGV, &old_sa, NULL);
    } else {
        cl_abort("Native call: wrong assigned types!\n");
    }


    if (count) {
        cl_free_memory(arg_types);
        for (size_t i = 0; i < count; i++) {
            cl_free_memory(variables[i]);
        }
    }

    CL_Object* ret_obj;
    if (!result) {
        cl_free_memory(result);
        return cl_make_unspecified();
    }

    switch (data->return_type) {
        HANDLE_RET_VALUE(CL_NATIVE_INTEGER, int, cl_make_int)
        HANDLE_RET_VALUE(CL_NATIVE_DOUBLE, double, cl_make_double)
        HANDLE_RET_VALUE(CL_NATIVE_CHAR, char, cl_make_char)
        HANDLE_RET_VALUE(CL_NATIVE_STRING, char*, cl_make_string)

        default:
            cl_abort("Native call result unknown type!\n");
            __builtin_unreachable();
    }

    cl_free_memory(result);
    return ret_obj;
}

CL_Object* cl_native(const char* func, const char* library, enum CL_NativeType result_type, unsigned int count, ...) {
    va_list args;
    va_start(args, count);

    CL_NativeData* data = cl_allocate_memory(sizeof(CL_NativeData));
    data->func = get_function(func, library);
    data->return_type = result_type;
    data->count = count;
    if (count) {
        data->args_types = cl_allocate_memory(sizeof(enum CL_NativeType) * count);
    } else {
        data->args_types = NULL;
    }

    for (unsigned int i = 0; i < count; i++) {
        enum CL_NativeType type = va_arg(args, enum CL_NativeType);
        data->args_types[i] = type;
    }

    va_end(args);
    return cl_make_lambda_native(cl_call_native, data);
}

void cl_destroy_native_data(CL_NativeData* data) {
    if (data->args_types) {
        cl_free_memory(data->args_types);
    }
    cl_free_memory(data);
}
