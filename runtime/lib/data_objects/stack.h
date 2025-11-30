#pragma once
#include <stddef.h>

#include "dynamic_array.h"

typedef struct {
    CL_DynamicArray* data;
    size_t top;
} CL_Stack;

CL_Stack* cl_stack_create();

void cl_stack_push(CL_Stack *stack, void *data);

void* cl_stack_pop(CL_Stack *stack);

void* cl_stack_peek(CL_Stack *stack);

void cl_stack_destroy(CL_Stack *stack);
