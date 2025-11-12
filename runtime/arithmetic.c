#include "arithmetic.h"

#include "const.h"

Object* clisp_add(const int count, Object** args) {
    // TODO:
    int sum = 0;
    for (int i = 0; i < count; i++) {
        const IntValue* v1 = args[i]->value;
        sum += v1->value;
    }

    return make_int(sum);
}
