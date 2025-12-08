#include "list.h"

#include "lib/memory.h"
#include "pair.h"
#include "primitive.h"
#include "utils.h"

CL_Object* cl_make_list(CL_FUNC_PARAMS) {
    CL_EmptyListObject* empty_list_object = cl_allocate_memory(sizeof(CL_EmptyListObject));
    cl_init_obj((CL_Object*)empty_list_object, EMPTY_LIST);

    if (!count) {
        return (CL_Object*)empty_list_object;
    }

    CL_PairObject* result = NULL;
    CL_PairObject* curr_pair = NULL;
    for (unsigned int i = 0; i < count; i++) {
        CL_PairObject* new_pair = (CL_PairObject*)cl_make_pair_internal(args[i], (CL_Object*)empty_list_object);
        if (!result) {
            result = new_pair;
            curr_pair = new_pair;
            continue;
        }

        // cl_set_pair_right_internal_weak not increases count of refs for new object.
        // This ensures that in the new list, all internal pairs will have 1 reference.
        cl_set_pair_right_internal_weak((CL_Object*)curr_pair, (CL_Object*)new_pair);
        curr_pair = new_pair;
    }

    // After resets in cycle upper count of refs = 2. Decrease it to 1.
    cl_decrease_ref_count((CL_Object*)empty_list_object);

    return (CL_Object*)result;
}

unsigned char cl_is_list_internal(CL_Object* obj) {
    CL_Object* curr_obj = obj;
    while (curr_obj != NULL) {
        enum CL_ObjectType type = cl_get_obj_type(curr_obj);

        if (type == EMPTY_LIST) {
            return TRUE;
        }

        if (type != PAIR) {
            return FALSE;
        }

        curr_obj = cl_get_pair_right_internal(curr_obj);
    }

    return FALSE;
}

CL_Object* cl_is_list(CL_FUNC_PARAMS) {
    CL_CHECK_FUNC_ARGS_COUNT(count, 1, EQUAL);
    return cl_make_boolean(cl_is_list_internal(args[0]));
}

CL_Object* cl_list_at(CL_FUNC_PARAMS) {
    CL_CHECK_FUNC_ARGS_COUNT(count, 2, EQUAL);
    CL_CHECK_FUNC_ARG_TYPE(cl_get_obj_type(args[1]), INTEGER);

    CL_Object* list = args[0];
    CL_Object* pos = args[1];

    if (cl_get_obj_type(list) == EMPTY_LIST) {
        cl_abort("List is empty!\n");
        __builtin_unreachable();
    }

    CL_Object* curr_pair = list;
    int rest = cl_get_int_value(pos);

    if (rest < 0) {
        cl_abort("Position is negative!\n");
    }

    while (rest > 0 && cl_get_obj_type(curr_pair) != EMPTY_LIST) {
        if (cl_get_obj_type(curr_pair) != PAIR) {
            cl_abort("Object is not a list!\n");
            __builtin_unreachable();
        }

        curr_pair = cl_get_pair_right_internal(curr_pair);
        rest--;
    }

    if (rest > 0 || cl_get_obj_type(curr_pair) == EMPTY_LIST) {
        cl_abort("Not found in list!\n");
        __builtin_unreachable();
    }
    cl_increase_ref_count(cl_get_pair_left_internal(curr_pair));
    return cl_get_pair_left_internal(curr_pair);
}

CL_Object* cl_list_length(CL_FUNC_PARAMS) {
    CL_CHECK_FUNC_ARGS_COUNT(count, 1, EQUAL);
    CL_Object* list = args[0];

    if (cl_get_obj_type(list) == EMPTY_LIST) {
        return cl_make_int(0);
    }

    int length = 0;
    CL_Object* curr_pair = list;
    while (cl_get_obj_type(curr_pair) != EMPTY_LIST) {
        if (cl_get_obj_type(curr_pair) != PAIR) {
            cl_abort("Object is not a list!\n");
            __builtin_unreachable();
        }
        curr_pair = cl_get_pair_right_internal(curr_pair);
        length++;
    }

    return cl_make_int(length);
}

void cl_destroy_empty_list(CL_Object* obj) {
    cl_free_memory(obj);
}
