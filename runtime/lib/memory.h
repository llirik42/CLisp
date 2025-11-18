#pragma once
#include <stddef.h>

void* allocate_memory(size_t size);

void* reallocate_memory(void* ptr, size_t size);

void free_memory(void* ptr);
