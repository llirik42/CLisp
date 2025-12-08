#include <assert.h>

#include "core.h"
#include "utils.h"

#include "lib/objects/primitive.h"
#include "lib/objects/evaluable.h"
#include "lib/objects/lambda.h"
#include "lib/objects/list.h"
#include "lib/objects/pair.h"
#include "lib/objects/vector.h"
#include "lib/memory/memory.h"

CL_Object* cl_make_unspecified() {
    CL_Object* obj = cl_allocate_memory(sizeof(CL_Object));
    cl_init_obj(obj, UNSPECIFIED);
    return obj;
}

void cl_init_obj(CL_Object* obj, enum CL_ObjectType type) {
    obj->type = type;
    obj->ref_count = 1;
}

void cl_inc_refs_cnt(CL_Object* obj) {
    obj->ref_count++;
}

static void cl_destroy_unspecified(CL_Object* obj) {
    cl_free_memory(obj);
}

void cl_dec_refs_cnt(CL_Object* obj) {
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
        case VECTOR:
            cl_destroy_vector(obj);
            break;
        case EVALUABLE:
            cl_destroy_evaluable(obj);
            break;
        case LAMBDA:
            cl_destroy_lambda(obj);
            break;
        case UNSPECIFIED:
            cl_destroy_unspecified(obj);
            break;
        case PAIR:
            cl_destroy_pair(obj);
            break;
        case EMPTY_LIST:
            cl_destroy_empty_list(obj);
            break;
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
        case VECTOR:
            return "VECTOR";
        case LAMBDA:
            return "LAMBDA";
        case UNSPECIFIED:
            return "UNSPECIFIED";
        case PAIR:
            return "PAIR";
        case EMPTY_LIST:
            return "EMPTY_LIST";
    }
    return "UNKNOWN";
}

enum CL_ObjectType cl_get_obj_type(CL_Object* obj) {
    return obj->type;
}

bool cl_is_numeric_internal(enum CL_ObjectType type) {
    return type == INTEGER || type == DOUBLE;
}

bool cl_obj_to_boolean(CL_Object* obj) {
    assert(cl_get_obj_type(obj) != EVALUABLE);

    if (cl_get_obj_type(obj) == BOOLEAN) {
        return cl_get_boolean_value(obj);
    }

    return true;
}

CL_Object* cl_is_numeric(CL_FUNC_PARAMS) {
    CL_CHECK_FUNC_ARGS_COUNT(1, count, EQUAL);
    return cl_make_boolean(cl_is_numeric_internal(cl_get_obj_type(args[0])));
}

CL_Object* cl_is_integer(CL_FUNC_PARAMS) {
    CL_CHECK_FUNC_ARGS_COUNT(1, count, EQUAL);
    return cl_make_boolean(cl_get_obj_type(args[0]) == INTEGER);
}

CL_Object* cl_is_double(CL_FUNC_PARAMS) {
    CL_CHECK_FUNC_ARGS_COUNT(1, count, EQUAL);
    return cl_make_boolean(cl_get_obj_type(args[0]) == DOUBLE);
}

CL_Object* cl_is_string(CL_FUNC_PARAMS) {
    CL_CHECK_FUNC_ARGS_COUNT(1, count, EQUAL);
    return cl_make_boolean(cl_get_obj_type(args[0]) == STRING);
}

CL_Object* cl_is_char(CL_FUNC_PARAMS) {
    CL_CHECK_FUNC_ARGS_COUNT(1, count, EQUAL);
    return cl_make_boolean(cl_get_obj_type(args[0]) == CHAR);
}

CL_Object* cl_is_boolean(CL_FUNC_PARAMS) {
    CL_CHECK_FUNC_ARGS_COUNT(1, count, EQUAL);
    return cl_make_boolean(cl_get_obj_type(args[0]) == BOOLEAN);
}

CL_Object* cl_is_procedure(CL_FUNC_PARAMS) {
    CL_CHECK_FUNC_ARGS_COUNT(1, count, EQUAL);
    return cl_make_boolean(cl_get_obj_type(args[0]) == LAMBDA);
}

CL_Object* cl_is_evaluable(CL_FUNC_PARAMS) {
    CL_CHECK_FUNC_ARGS_COUNT(1, count, EQUAL);
    return cl_make_boolean(cl_get_obj_type(args[0]) == EVALUABLE);
}
