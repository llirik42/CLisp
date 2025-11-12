#include "runtime.h"

int main() {
    Object* var1 = make_int(4);
    Object* var2 = make_int(3);
    Object* var3 = make_int(10);
    Object* list1[] = {var1, var2, var3};
    Object* var4 = make_evaluable(clisp_add, 3, list1);
    Object* var5 = evaluate(var4);

    clisp_display(var5);
    destroy(var5);
    destroy(var4);
    destroy(var3);
    destroy(var2);
    destroy(var1);
    return 0;
}