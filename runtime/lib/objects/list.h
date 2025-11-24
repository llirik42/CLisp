#pragma once
#include "lib/data_objects/dynamic_array.h"
#include "lib/core.h"

#define UNDEFINED_SIZE 0

typedef struct {
    enum ObjectType type;
    unsigned short ref_count;
    DynamicArray* list;
} ListObject;

Object* clisp_make_list();

Object* clisp_make_list_capacity(size_t size);

void clisp_list_append(Object* list, Object* obj);

Object* clisp_list_at(Object* list, size_t index);

size_t clisp_list_length(Object* list);

Object* clisp_make_list_from_array(unsigned int size, Object** array);

void destroy_list(Object* obj);
