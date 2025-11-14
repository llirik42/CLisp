#include "logic.h"

#include <stdio.h>
#include <string.h>

#include "const.h"
#include "evaluable.h"
#include "utils.h"

Object* clisp_if(CLISP_FUNC_PARAMS) {
    if (count < 1 || count > 3) {
        char error[128];
        snprintf(error, 128, "Invalid number of arguments passed to clisp_if! Expected 2 or 3. Got %d\n", count);
        print_error_and_exit(error, 0);
    }

    unsigned char test_value = obj_to_boolean(args[0]);
    Object* consequent = args[1];
    Object* alternative = args[2];

    if (test_value) {
        return evaluate(consequent);
    }

    if (count == 2) {
        return make_unspecified();
    }

    return evaluate(alternative);
}

Object* clisp_not(CLISP_FUNC_PARAMS) {
    CHECK_FUNC_ARGUMENTS_COUNT(count, 1, EQUAL);

    Object* term = evaluate(args[0]);

    if (obj_to_boolean(term)) {
        return make_false();
    }
    return make_true();
}

Object* clisp_or(CLISP_FUNC_PARAMS) {

    if (count == 0) {
        return make_false();
    }

    for (unsigned int i = 0; i < count - 1; i++) {
        Object* statement = evaluate(args[i]);

        // 1 v A = 1
        if (obj_to_boolean(statement)) {
            return make_true();
        }
    }

    Object* last_statement = evaluate(args[count - 1]);

    if (obj_to_boolean(last_statement)) {
        return make_true();
    }

    return make_false();
}

Object* clisp_and(CLISP_FUNC_PARAMS) {

    if (count == 0) {
        return make_true();
    }

    for (unsigned int i = 0; i < count - 1; i++) {
        Object* statement = evaluate(args[i]);

        // 0 & A = 1
        if (!obj_to_boolean(statement)) {
            return make_false();
        }
    }

    Object* last_statement = evaluate(args[count - 1]);

    if (obj_to_boolean(last_statement)) {
        return make_true();
    }

    return make_false();
}