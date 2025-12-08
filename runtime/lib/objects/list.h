#pragma once
#include "lib/core.h"

typedef struct {
    enum CL_ObjectType type;
    unsigned short ref_count;
} CL_EmptyListObject;

CL_Object* cl_make_list(CL_FUNC_PARAMS);

CL_Object* cl_is_list(CL_FUNC_PARAMS);

bool cl_is_list_internal(CL_Object* obj);

CL_Object* cl_list_at(CL_FUNC_PARAMS);

unsigned int cl_list_length_internal(CL_Object* obj);

CL_Object* cl_list_length(CL_FUNC_PARAMS);

void cl_destroy_empty_list(CL_Object* obj);
