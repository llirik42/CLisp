#pragma once
#include <stddef.h>

void* cl_allocate_memory(size_t size);

void* cl_reallocate_memory(void* ptr, size_t size);

void cl_free_memory(void* ptr);
