#pragma once
#include <stddef.h>

void* allocate_memory(size_t size);

void free_memory(void* ptr);
