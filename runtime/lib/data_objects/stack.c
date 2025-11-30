#include "stack.h"

#include "memory.h"
#include "utils.h"

#define DEFAULT_STACK_SIZE 8

CL_Stack* cl_stack_create() {
    CL_Stack* stack = cl_allocate_memory(sizeof(CL_Stack));
    stack->data = cl_da_create(DEFAULT_STACK_SIZE);
    stack->top = 0;
    return stack;
}

void cl_stack_push(CL_Stack *stack, void *data) {
    cl_da_append(stack->data, data);
    stack->top++;
}

void* cl_stack_pop(CL_Stack *stack) {
    if (stack->top == 0) {
        cl_abort("Stack underflow!\n");
        __builtin_unreachable();
    }

    void* data = cl_da_get(stack->data, --stack->top);
    cl_da_pop(stack->data);
    return data;
}

void* cl_stack_peek(CL_Stack *stack) {
    if (stack->top <= 0) {
        cl_abort("Stack underflow!\n");
        __builtin_unreachable();
    }

    return cl_da_get(stack->data, stack->top - 1);
}

void cl_stack_destroy(CL_Stack *stack) {
    cl_da_destroy(stack->data);
}
