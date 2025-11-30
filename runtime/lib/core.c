#include "core.h"
#include "memory.h"

#include "objects/primitive.h"
#include "objects/evaluable.h"
#include "objects/lambda.h"
#include "objects/list.h"

CL_Object* cl_make_unspecified() {
    CL_Object* obj = allocate_memory(sizeof(CL_Object));
    cl_init_obj(obj, UNSPECIFIED);
    return obj;
}

void cl_init_obj(CL_Object* obj, enum CL_ObjectType type) {
    obj->type = type;
    obj->ref_count = 1;
}

void cl_increase_refs_count(CL_Object* obj) {
    obj->ref_count++;
}

static void destroy_unspecified(CL_Object* obj) {
    free_memory(obj);
}

void cl_destroy_object(CL_Object* obj) {
    if (!obj || !obj->ref_count) {
        return;
    }

    if (--obj->ref_count > 0) {
        return;
    }

    switch (cl_get_obj_type(obj)) {
        case INTEGER:
            cl_destroy_int(obj);
            break;
        case DOUBLE:
            cl_destroy_double(obj);
            break;
        case BOOLEAN:
            cl_destroy_boolean(obj);
            break;
        case STRING:
            cl_destroy_string(obj);
            break;
        case CHAR:
            cl_destroy_char(obj);
            break;
        case LIST:
            cl_destroy_list(obj);
            break;
        case EVALUABLE:
            cl_destroy_evaluable(obj);
            break;
        case LAMBDA:
            cl_destroy_lambda(obj);
            break;
        case UNSPECIFIED:
            destroy_unspecified(obj);
        default: ;
    }
}

char* get_obj_type_name(enum CL_ObjectType type) {
    switch(type) {
        case INTEGER:
            return "INTEGER";
        case DOUBLE:
            return "DOUBLE";
        case BOOLEAN:
            return "BOOLEAN";
        case EVALUABLE:
            return "EVALUABLE";
        case STRING:
            return "STRING";
        case CHAR:
            return "CHAR";
        case LIST:
            return "LIST";
        case LAMBDA:
            return "LAMBDA";
        case UNSPECIFIED:
            return "UNSPECIFIED";
    }
    return "UNKNOWN";
}

enum CL_ObjectType cl_get_obj_type(CL_Object* obj) {
    return obj->type;
}

unsigned char cl_is_numeric(enum CL_ObjectType type) {
    return type == INTEGER || type == DOUBLE;
}
