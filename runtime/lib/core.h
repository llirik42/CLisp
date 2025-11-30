#pragma once

#define TRUE 1
#define FALSE 0

enum CL_ObjectType {
    INTEGER,
    DOUBLE,
    BOOLEAN,
    EVALUABLE,
    STRING,
    CHAR,
    LIST,
    LAMBDA,
    UNSPECIFIED,
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

void cl_increase_refs_count(CL_Object* obj);

CL_Object* cl_make_unspecified();

void cl_destroy_object(CL_Object* obj);

unsigned char cl_is_numeric(enum CL_ObjectType type);
