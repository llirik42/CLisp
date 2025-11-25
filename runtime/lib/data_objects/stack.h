#pragma once
#include <stddef.h>

#include "dynamic_array.h"

typedef struct {
    DynamicArray* data;
    size_t top;
} Stack;

Stack* stack_create();

void stack_push(Stack *stack, void *data);

void* stack_pop(Stack *stack);

void* stack_peek(Stack *stack);

void stack_destroy(Stack *stack);
