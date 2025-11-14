#include "io.h"

#include <stdio.h>

#include "const.h"
#include "core.h"
#include "evaluable.h"
#include "utils.h"

Object* clisp_display(CLISP_FUNC_PARAMS) {
    CHECK_FUNC_ARGUMENTS_COUNT(count, 1, EQUAL);

    Object* to_display = evaluate(args[0]);

    switch (get_object_type(to_display)) {
        case INTEGER:
            printf("%d\n", get_int_value(to_display));
            break;
        case DOUBLE:
            printf("%f\n", get_double_value(to_display));
            break;
        case STRING:
            printf("%s\n", get_string_value(to_display));
            break;
        case CHAR:
            printf("%c\n", get_char_value(to_display));
            break;
        case BOOLEAN:
            if (get_boolean_value(to_display)) {
                printf("true\n");
            } else {
                printf("false\n");
            }
            break;
        case UNSPECIFIED:
            printf("unspecified\n");
            break;
        default:
            printf("Undisplayable type\n");
    }

    return make_unspecified();
}
