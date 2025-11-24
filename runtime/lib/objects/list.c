#include "list.h"

#include "lib/memory.h"

#define UNDEFINED_SIZE 0

static Object* make_list(size_t size) {
    ListObject* list_object = allocate_memory(sizeof(ListObject));
    init_object((Object*)list_object, LIST);

    list_object->list = da_create(size);
    return (Object*)list_object;
}

Object* clisp_make_list() {
    return make_list(UNDEFINED_SIZE);
}

Object* clisp_make_list_capacity(size_t size) {
    return make_list(size);
}

void clisp_list_append(Object* list, Object* obj) {
    const ListObject* list_object = (ListObject*)list;
    da_push_back(list_object->list, obj);
}

Object* clisp_list_at(Object* list, size_t index) {
    // TODO: Сейчас da_get вызовет abort на index out of range. Здесь можно выкидывать исключение.

    const ListObject* list_object = (ListObject*)list;
    return da_get(list_object->list, index);
}

size_t clisp_list_length(Object* list) {
    const ListObject* list_object = (ListObject*)list;
    return da_size(list_object->list);
}

Object* clisp_make_list_from_array(unsigned int size, Object** array) {
    ListObject* list_object = allocate_memory(sizeof(ListObject));
    init_object((Object*)list_object, LIST);

    list_object->list = da_create(size);

    for (size_t i = 0; i < size; i++) {
        da_push_back(list_object->list, array[i]);
    }

    return (Object*)list_object;
}

void destroy_list(Object* obj) {
    const ListObject* list_object = (ListObject*)obj;
    da_destroy(list_object->list);
    free_memory(obj);
}
