#pragma once
#include <stdbool.h>

enum CL_ObjectType {
    INTEGER,
    DOUBLE,
    BOOLEAN,
    EVALUABLE,
    STRING,
    CHAR,
    VECTOR,
    LAMBDA,
    UNSPECIFIED,
    PAIR,
    EMPTY_LIST,
};

char* get_obj_type_name(enum CL_ObjectType type);

typedef struct {
    enum CL_ObjectType type;
    unsigned short ref_count;
} CL_Object;

#define CL_FUNC_PARAMS unsigned int count, CL_Object** args
#define CL_FUNC_PARAMS_WITHOUT_TYPES count, args

typedef CL_Object*(*cl_func)(CL_FUNC_PARAMS);

enum CL_ObjectType cl_get_obj_type(CL_Object* obj);

void cl_init_obj(CL_Object* obj, enum CL_ObjectType type);

void cl_increase_ref_count(CL_Object* obj);

void cl_decrease_ref_count(CL_Object* obj);

CL_Object* cl_make_unspecified();

bool cl_is_numeric_internal(enum CL_ObjectType type);

bool cl_obj_to_boolean(CL_Object* obj);

CL_Object* cl_is_numeric(CL_FUNC_PARAMS);

CL_Object* cl_is_integer(CL_FUNC_PARAMS);

CL_Object* cl_is_double(CL_FUNC_PARAMS);

CL_Object* cl_is_string(CL_FUNC_PARAMS);

CL_Object* cl_is_char(CL_FUNC_PARAMS);

CL_Object* cl_is_boolean(CL_FUNC_PARAMS);

CL_Object* cl_is_procedure(CL_FUNC_PARAMS);

CL_Object* cl_is_evaluable(CL_FUNC_PARAMS);
