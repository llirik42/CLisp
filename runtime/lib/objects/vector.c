#include "vector.h"

#include "lib/memory.h"

#define UNDEFINED_SIZE 0

static CL_Object* make_list(size_t size) {
    CL_VectorObject* list_object = cl_allocate_memory(sizeof(CL_VectorObject));
    cl_init_obj((CL_Object*)list_object, VECTOR);

    list_object->list = cl_da_create(size);
    return (CL_Object*)list_object;
}

CL_Object* cl_make_vector() {
    return make_list(UNDEFINED_SIZE);
}

CL_Object* cl_make_vector_capacity(size_t size) {
    return make_list(size);
}

void cl_vector_append(CL_Object* list, CL_Object* obj) {
    const CL_VectorObject* list_object = (CL_VectorObject*)list;
    cl_da_append(list_object->list, obj);
}

CL_Object* cl_vector_at(CL_Object* list, size_t index) {
    // TODO: Сейчас da_get вызовет abort на index out of range. Здесь можно выкидывать исключение.

    const CL_VectorObject* list_object = (CL_VectorObject*)list;
    return cl_da_get(list_object->list, index);
}

size_t cl_vector_length(CL_Object* list) {
    const CL_VectorObject* list_object = (CL_VectorObject*)list;
    return cl_da_size(list_object->list);
}

CL_Object* cl_make_vector_from_array(unsigned int size, CL_Object** array) {
    CL_VectorObject* list_object = cl_allocate_memory(sizeof(CL_VectorObject));
    cl_init_obj((CL_Object*)list_object, VECTOR);

    list_object->list = cl_da_create(size);

    for (size_t i = 0; i < size; i++) {
        cl_da_append(list_object->list, array[i]);
    }

    return (CL_Object*)list_object;
}

void cl_destroy_vector(CL_Object* obj) {
    const CL_VectorObject* list_object = (CL_VectorObject*)obj;
    cl_da_destroy(list_object->list);
    cl_free_memory(obj);
}
