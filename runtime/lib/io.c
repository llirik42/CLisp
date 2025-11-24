#include "io.h"

#include <stdio.h>

#include "lib/objects/primitive.h"
#include "core.h"
#include "utils.h"
#include "lib/objects/list.h"

static void display_one_object(Object* obj) {
    Object* to_display = unwrap_object(obj);

    switch (get_object_type(to_display)) {
        case INTEGER:
            printf("%d", get_int_value(to_display));
            break;
        case DOUBLE:
            printf("%g", get_double_value(to_display));
            break;
        case STRING:
            printf("%s", get_string_value(to_display));
            break;
        case CHAR:
            printf("%c", get_char_value(to_display));
            break;
        case BOOLEAN:
            if (get_boolean_value(to_display)) {
                printf("true");
            } else {
                printf("false");
            }
            break;
        case LIST:
            printf("%s", "list(");
            for (size_t i = 0; i < clisp_list_length(to_display); i++) {
                display_one_object(clisp_list_at(to_display, i));
                if (i != clisp_list_length(to_display) - 1) {
                    putchar(' ');
                }
            }
            putchar(')');
            break;
        case UNSPECIFIED:
            printf("unspecified");
            break;
        default:
            printf("Undisplayable type");
    }

    destroy_if_unwrapped(obj, to_display);
}

Object* clisp_display(CLISP_FUNC_PARAMS) {
    CHECK_FUNC_ARGUMENTS_COUNT(count, 0, GREATER);

    for (unsigned int i = 0; i < count; i++) {
        display_one_object(args[i]);
        if (i != count - 1) {
            putchar(' ');
        }
    }

    putchar('\n');

    return clisp_make_unspecified();
}
