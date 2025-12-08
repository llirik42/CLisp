#pragma once
#include "lib/core/core.h"

typedef struct {
    enum CL_ObjectType type;
    unsigned short ref_count;
    CL_Object* left;
    CL_Object* right;
} CL_PairObject;

CL_Object* cl_make_pair_internal(CL_Object* left, CL_Object* right);

CL_Object* cl_make_pair(CL_FUNC_PARAMS);

CL_Object* cl_is_pair(CL_FUNC_PARAMS);

CL_Object* cl_get_pair_left(CL_FUNC_PARAMS);

CL_Object* cl_get_pair_right(CL_FUNC_PARAMS);

CL_Object* cl_get_pair_left_internal(CL_Object* obj);

CL_Object* cl_get_pair_right_internal(CL_Object* obj);

CL_Object* cl_set_pair_left(CL_FUNC_PARAMS);

CL_Object* cl_set_pair_right(CL_FUNC_PARAMS);

void cl_set_pair_left_internal(CL_Object* obj, CL_Object* new);

void cl_set_pair_right_internal_weak(CL_Object* obj, CL_Object* new);

void cl_destroy_pair(CL_Object* obj);
