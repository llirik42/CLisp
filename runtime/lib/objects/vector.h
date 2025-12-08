#pragma once
#include "lib/data_objects/dynamic_array.h"
#include "lib/core.h"

typedef struct {
    enum CL_ObjectType type;
    unsigned short ref_count;
    CL_DynamicArray* list;
} CL_VectorObject;

CL_Object* cl_make_vector();

CL_Object* cl_make_vector_capacity(size_t size);

void cl_vector_append(CL_Object* list, CL_Object* obj);

CL_Object* cl_vector_at(CL_Object* list, size_t index);

size_t cl_vector_length(CL_Object* list);

CL_Object* cl_make_vector_from_array(unsigned int size, CL_Object** array);

void cl_destroy_vector(CL_Object* obj);
