#include "../runtime.h"

int main() {

    Object* var1 = make_int(1);
    Object* var2 = make_int(2);
    Object* var3 = make_int(6);

    Object* list1[] = {var1, var2, var3};
    Object* var4 = make_evaluable(clisp_add, 3, list1);
    Object* var5 = evaluate(var4);
    clisp_display(var5);

    return 0;
}
