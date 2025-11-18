#include "logic.h"

#include <stdio.h>

#include "primitive.h"
#include "utils.h"

Object* clisp_if(CLISP_FUNC_PARAMS) {
    if (count < 1 || count > 3) {
        char error[128];
        snprintf(error, 128, "Invalid number of arguments passed to clisp_if! Expected 2 or 3. Got %d\n", count);
        print_error_and_exit(error, 0);
    }

    unsigned char test_value = obj_to_boolean(args[0]);

    if (test_value) {
        Object* consequent = unwrap_object(args[1]);
        if (consequent == args[1]) {
            increase_refs_count(consequent);
        }
        return consequent;
    }

    if (count == 2) {
        return clisp_make_unspecified();
    }

    Object* alternative = unwrap_object(args[2]);
    if (alternative == args[2]) {
        increase_refs_count(alternative);
    }
    return alternative;
}

Object* clisp_not(CLISP_FUNC_PARAMS) {
    CHECK_FUNC_ARGUMENTS_COUNT(count, 1, EQUAL);

    Object* term = unwrap_object(args[0]);
    unsigned char term_value = obj_to_boolean(term);
    destroy_if_unwrapped(args[0], term);

    if (term_value) {
        return make_false();
    }
    return make_true();
}

Object* clisp_or(CLISP_FUNC_PARAMS) {
    if (count == 0) {
        return make_false();
    }

    for (unsigned int i = 0; i < count - 1; i++) {
        Object* statement = unwrap_object(args[i]);
        unsigned char statement_value = obj_to_boolean(statement);
        destroy_if_unwrapped(args[i], statement);
        // 1 v A = 1
        if (statement_value) {
            return make_true();
        }
    }

    Object* last_statement = unwrap_object(args[count - 1]);
    unsigned char statement_value = obj_to_boolean(last_statement);
    destroy_if_unwrapped(args[count - 1], last_statement);
    if (statement_value) {
        return make_true();
    }

    return make_false();
}

Object* clisp_and(CLISP_FUNC_PARAMS) {
    if (count == 0) {
        return make_true();
    }

    for (unsigned int i = 0; i < count - 1; i++) {
        Object* statement = unwrap_object(args[i]);
        unsigned char statement_value = obj_to_boolean(statement);
        destroy_if_unwrapped(args[i], statement);

        // 0 & A = 1
        if (!statement_value) {
            return make_false();
        }
    }

    Object* last_statement = unwrap_object(args[count - 1]);
    unsigned char statement_value = obj_to_boolean(last_statement);
    destroy_if_unwrapped(args[count - 1], last_statement);

    if (statement_value) {
        return make_true();
    }

    return make_false();
}
