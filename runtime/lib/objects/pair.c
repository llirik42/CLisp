#include "pair.h"

#include "list.h"
#include "primitive.h"
#include "utils.h"
#include "lib/memory.h"

CL_Object* cl_make_pair_internal(CL_Object* left, CL_Object* right) {
    CL_PairObject* pair_object = cl_allocate_memory(sizeof(CL_PairObject));
    cl_init_obj((CL_Object*)pair_object, PAIR);

    pair_object->left = left;
    pair_object->right = right;
    cl_increase_ref_count(left);
    cl_increase_ref_count(right);

    return (CL_Object*)pair_object;
}

CL_Object* cl_make_pair(CL_FUNC_PARAMS) {
    CL_CHECK_FUNC_ARGS_COUNT(count, 2, EQUAL);
    return cl_make_pair_internal(args[0], args[1]);
}

CL_Object* cl_is_pair(CL_FUNC_PARAMS) {
    CL_CHECK_FUNC_ARGS_COUNT(count, 1, EQUAL);
    return cl_make_boolean(cl_get_obj_type(args[0]) == PAIR);
}

CL_Object* cl_get_pair_left(CL_FUNC_PARAMS) {
    CL_CHECK_FUNC_ARGS_COUNT(count, 1, EQUAL);
    CL_CHECK_FUNC_ARG_TYPE(cl_get_obj_type(args[0]), PAIR);
    CL_PairObject* pair_object = (CL_PairObject*)args[0];
    cl_increase_ref_count(pair_object->left);
    return pair_object->left;
}

CL_Object* cl_get_pair_right(CL_FUNC_PARAMS) {
    CL_CHECK_FUNC_ARGS_COUNT(count, 1, EQUAL);
    CL_CHECK_FUNC_ARG_TYPE(cl_get_obj_type(args[0]), PAIR);
    CL_PairObject* pair_object = (CL_PairObject*)args[0];
    cl_increase_ref_count(pair_object->right);
    return pair_object->right;
}

CL_Object* cl_get_pair_left_internal(CL_Object* obj) {
    CL_PairObject* pair_object = (CL_PairObject*)obj;
    return pair_object->left;
}

CL_Object* cl_get_pair_right_internal(CL_Object* obj) {
    CL_PairObject* pair_object = (CL_PairObject*)obj;
    return pair_object->right;
}

CL_Object* cl_set_pair_left(CL_FUNC_PARAMS) {
    CL_CHECK_FUNC_ARGS_COUNT(count, 2, EQUAL);
    CL_CHECK_FUNC_ARG_TYPE(cl_get_obj_type(args[0]), PAIR);
    CL_PairObject* pair_object = (CL_PairObject*)args[0];
    cl_decrease_ref_count(pair_object->left);
    cl_increase_ref_count(args[1]);
    pair_object->left = args[1];
    return cl_make_unspecified();
}

CL_Object* cl_set_pair_right(CL_FUNC_PARAMS) {
    CL_CHECK_FUNC_ARGS_COUNT(count, 2, EQUAL);
    CL_CHECK_FUNC_ARG_TYPE(cl_get_obj_type(args[0]), PAIR);
    CL_PairObject* pair_object = (CL_PairObject*)args[0];
    cl_decrease_ref_count(pair_object->right);
    cl_increase_ref_count(args[1]);
    pair_object->right = args[1];
    return cl_make_unspecified();
}

void cl_set_pair_left_internal(CL_Object* obj, CL_Object* new) {
    CL_PairObject* pair_object = (CL_PairObject*)obj;
    cl_decrease_ref_count(pair_object->left);
    cl_increase_ref_count(new);
    pair_object->left = new;
}

void cl_set_pair_right_internal(CL_Object* obj, CL_Object* new) {
    CL_PairObject* pair_object = (CL_PairObject*)obj;
    cl_decrease_ref_count(pair_object->right);
    cl_increase_ref_count(new);
    pair_object->right = new;
}

void cl_set_pair_right_internal_weak(CL_Object* obj, CL_Object* new) {
    CL_PairObject* pair_object = (CL_PairObject*)obj;
    cl_decrease_ref_count(pair_object->right);
    pair_object->right = new;
}

void cl_destroy_pair(CL_Object* obj) {
    cl_decrease_ref_count(cl_get_pair_left_internal(obj));
    cl_decrease_ref_count(cl_get_pair_right_internal(obj));
    cl_free_memory(obj);
}
