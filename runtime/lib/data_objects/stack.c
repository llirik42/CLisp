#include "stack.h"

#include "memory.h"
#include "utils.h"

#define DEFAULT_STACK_SIZE 8

Stack* stack_create() {
    Stack* stack = allocate_memory(sizeof(Stack));
    stack->data = da_create(DEFAULT_STACK_SIZE);
    stack->top = 0;
    return stack;
}

void stack_push(Stack *stack, void *data) {
    da_append(stack->data, data);
    stack->top++;
}

void* stack_pop(Stack *stack) {
    if (stack->top == 0) {
        clisp_exit("Stack underflow!\n");
        __builtin_unreachable();
    }

    void* data = da_get(stack->data, --stack->top);
    da_pop(stack->data);
    return data;
}

void* stack_peek(Stack *stack) {
    if (stack->top <= 0) {
        clisp_exit("Stack underflow!\n");
        __builtin_unreachable();
    }

    return da_get(stack->data, stack->top - 1);
}

void stack_destroy(Stack *stack) {
    da_destroy(stack->data);
}
