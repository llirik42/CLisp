#pragma once
#include "lib/data_objects/dynamic_array.h"
#include "lib/core.h"

typedef struct {
    enum CL_ObjectType type;
    unsigned short ref_count;
    CL_DynamicArray* list;
} CL_ListObject;

CL_Object* cl_make_list();

CL_Object* cl_make_list_capacity(size_t size);

void cl_list_append(CL_Object* list, CL_Object* obj);

CL_Object* cl_list_at(CL_Object* list, size_t index);

size_t cl_list_length(CL_Object* list);

CL_Object* cl_make_list_from_array(unsigned int size, CL_Object** array);

void cl_destroy_list(CL_Object* obj);
