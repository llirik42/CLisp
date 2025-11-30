#include "list.h"

#include "lib/memory.h"

#define UNDEFINED_SIZE 0

static CL_Object* make_list(size_t size) {
    CL_ListObject* list_object = allocate_memory(sizeof(CL_ListObject));
    cl_init_obj((CL_Object*)list_object, LIST);

    list_object->list = cl_da_create(size);
    return (CL_Object*)list_object;
}

CL_Object* cl_make_list() {
    return make_list(UNDEFINED_SIZE);
}

CL_Object* cl_make_list_capacity(size_t size) {
    return make_list(size);
}

void cl_list_append(CL_Object* list, CL_Object* obj) {
    const CL_ListObject* list_object = (CL_ListObject*)list;
    cl_da_append(list_object->list, obj);
}

CL_Object* cl_list_at(CL_Object* list, size_t index) {
    // TODO: Сейчас da_get вызовет abort на index out of range. Здесь можно выкидывать исключение.

    const CL_ListObject* list_object = (CL_ListObject*)list;
    return cl_da_get(list_object->list, index);
}

size_t cl_list_length(CL_Object* list) {
    const CL_ListObject* list_object = (CL_ListObject*)list;
    return cl_da_size(list_object->list);
}

CL_Object* cl_make_list_from_array(unsigned int size, CL_Object** array) {
    CL_ListObject* list_object = allocate_memory(sizeof(CL_ListObject));
    cl_init_obj((CL_Object*)list_object, LIST);

    list_object->list = cl_da_create(size);

    for (size_t i = 0; i < size; i++) {
        cl_da_append(list_object->list, array[i]);
    }

    return (CL_Object*)list_object;
}

void cl_destroy_list(CL_Object* obj) {
    const CL_ListObject* list_object = (CL_ListObject*)obj;
    cl_da_destroy(list_object->list);
    free_memory(obj);
}
