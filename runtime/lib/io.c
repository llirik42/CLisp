#include "io.h"

#include <stdio.h>

#include "lib/objects/primitive.h"
#include "core.h"
#include "utils.h"
#include "lib/objects/list.h"

static void display_one_object(CL_Object* obj) {
    CL_Object* to_display = cl_unwrap_obj(obj);

    switch (cl_get_obj_type(to_display)) {
        case INTEGER:
            printf("%d", cl_get_int_value(to_display));
            break;
        case DOUBLE:
            printf("%g", cl_get_double_value(to_display));
            break;
        case STRING:
            printf("%s", cl_get_string_value(to_display));
            break;
        case CHAR:
            printf("%c", cl_get_char_value(to_display));
            break;
        case BOOLEAN:
            if (cl_get_boolean_value(to_display)) {
                printf("true");
            } else {
                printf("false");
            }
            break;
        case LIST:
            printf("%s", "list(");
            for (size_t i = 0; i < cl_list_length(to_display); i++) {
                display_one_object(cl_list_at(to_display, i));
                if (i != cl_list_length(to_display) - 1) {
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

    cl_destroy_if_unwrapped(obj, to_display);
}

CL_Object* cl_display(CL_FUNC_PARAMS) {
    CL_CHECK_FUNC_ARGS_COUNT(count, 0, GREATER);

    for (unsigned int i = 0; i < count; i++) {
        display_one_object(args[i]);
        if (i != count - 1) {
            putchar(' ');
        }
    }

    putchar('\n');

    return cl_make_unspecified();
}
