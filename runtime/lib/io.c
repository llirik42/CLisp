#include "io.h"

#include <stdio.h>
#include <stdlib.h>

#include "lib/objects/primitive.h"
#include "core.h"
#include "utils.h"
#include "lib/objects/vector.h"
#include "objects/list.h"
#include "objects/pair.h"

static void display_one_object(CL_Object* obj) {
    CL_Object* to_display = obj;

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
        case VECTOR:
            printf("%s", "vector(");
            for (size_t i = 0; i < cl_vector_length(to_display); i++) {
                display_one_object(cl_vector_at(to_display, i));
                if (i != cl_vector_length(to_display) - 1) {
                    putchar(' ');
                }
            }
            putchar(')');
            break;
        case UNSPECIFIED:
            printf("unspecified");
            break;
        case PAIR: {
            if (cl_is_list_internal(to_display)) {
                putchar('(');
                CL_Object* curr_pair = to_display;
                while (TRUE) {
                    display_one_object(cl_get_pair_left_internal(curr_pair));
                    curr_pair = cl_get_pair_right_internal(curr_pair);
                    if (cl_get_obj_type(curr_pair) != EMPTY_LIST) {
                        putchar(' ');
                    } else {
                        break;
                    }
                }
                putchar(')');
            } else {
                putchar('(');
                display_one_object(cl_get_pair_left_internal(to_display));
                putchar(' ');
                putchar('.');
                putchar(' ');
                display_one_object(cl_get_pair_right_internal(to_display));
                putchar(')');
            }
            break;
        }
        case EMPTY_LIST:
            printf("%s","()");
            break;
        default:
            printf("Undisplayable type");
    }
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

CL_Object* cl_display_newline(CL_FUNC_PARAMS) {
    CL_CHECK_FUNC_ARGS_COUNT(count, 0, EQUAL);
    if (args) {}
    putchar('\n');
    return cl_make_unspecified();
}

CL_Object* cl_readline(CL_FUNC_PARAMS) {
    CL_CHECK_FUNC_ARGS_COUNT(count, 0, EQUAL);
    if (args) {}

    char *line = NULL;
    size_t len = 0;
    CL_Object* obj = NULL;

    if (getline(&line, &len, stdin) != -1) {
        obj = cl_make_string(line);
    } else {
        cl_abort("Error during reading stdin or no EOF!\n");
    }

    // getline uses default malloc.
    free(line);

    if (obj == NULL) {
        cl_abort("Readline: no data!\n");
    }

    return obj;
}
