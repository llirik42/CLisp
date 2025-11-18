#include "runtime.h"

int main() {
	Environment* env1 = make_environment(NULL, 2);

	Object* var1 = make_int(2);
	Object* var2 = make_int(3);
	Object* var3_args[] = {var1, var2};
	Object* var3 = clisp_add(2, var3_args);
	destroy(var3);
	destroy(var2);
	destroy(var1);

	Object* var4 = make_int(1);
	set_variable_value(env1, "x", var4);

	Object* var5 = get_variable_value(env1, "x");
	Object* var6 = make_int(5);
	Object* var7_args[] = {var5, var6};
	Object* var7 = clisp_add(2, var7_args);
	destroy(var7);
	destroy(var6);

	Object* var8 = make_int(1);
	Object* var9 = update_variable_value(env1, "x", var8);
	Object* var10_args[] = {var9};
	Object* var10 = clisp_display(1, var10_args);
	destroy(var10);
	destroy(var9);

	Object* var11 = get_variable_value(env1, "x");
	Object* var12 = make_int(5);
	Object* var13_args[] = {var11, var12};
	Object* var13 = clisp_add(2, var13_args);
	destroy(var13);
	destroy(var12);

	Object* var14 = make_string("hello");
	set_variable_value(env1, "y", var14);

	Object* var15 = get_variable_value(env1, "y");
	Object* var16 = get_variable_value(env1, "x");
	Object* var17_args[] = {var15, var16};
	Object* var17 = clisp_add(2, var17_args);
	destroy(var17);

	Environment* env2 = make_environment(env1, 0);

	Object* var18 = get_variable_value(env2, "x");
	Object* var19_args[] = {var18};
	Object* var19 = clisp_display(1, var19_args);

	Object* var20 = get_variable_value(env2, "y");
	Object* var21_args[] = {var20};
	Object* var21 = clisp_display(1, var21_args);

	Object* var22 = make_int(9);
	Object* var23 = update_variable_value(env2, "y", var22);
	Object* var24_args[] = {var23};
	Object* var24 = clisp_display(1, var24_args);

	Object* var25 = get_variable_value(env2, "x");
	Object* var26 = get_variable_value(env2, "y");
	Object* var27_args[] = {var25, var26};
	Object* var27 = clisp_add(2, var27_args);

	Object* var28_args[] = {var27};
	Object* var28 = clisp_display(1, var28_args);
	destroy(var28);

	destroy(var27);
	destroy(var24);
	destroy(var23);
	destroy(var22);
	destroy(var21);
	destroy(var19);
	destroy_environment(env2);

	Object* var29 = make_int(1);
	Object* var30 = make_int(2);
	Object* var31 = make_int(3);
	Object* var32 = make_int(4);
	Object* var33 = make_int(5);
	Object* var34 = make_int(6);
	Object* var35 = make_int(7);
	Object* var36_args[] = {var29, var30, var31, var32, var33, var34, var35};
	Object* var36 = clisp_add(7, var36_args);
	destroy(var36);
	destroy(var35);
	destroy(var34);
	destroy(var33);
	destroy(var32);
	destroy(var31);
	destroy(var30);
	destroy(var29);

	Environment* env3 = make_environment(env1, 2);
	Object* var37 = make_int(1);
	set_variable_value(env3, "a", var37);
	Object* var38 = make_int(2);
	set_variable_value(env3, "b", var38);

	Object* var39 = get_variable_value(env3, "a");
	Object* var40 = get_variable_value(env3, "b");
	Object* var41 = get_variable_value(env3, "x");
	Object* var42 = get_variable_value(env3, "y");
	Object* var43_args[] = {var39, var40, var41, var42};
	Object* var43 = clisp_add(4, var43_args);

	Object* var44 = make_int(10);
	Object* var45 = update_variable_value(env3, "a", var44);

	Object* var46 = make_int(5);
	Object* var47 = update_variable_value(env3, "x", var46);

	Object* var48 = get_variable_value(env3, "a");
	Object* var49 = get_variable_value(env3, "b");
	Object* var50 = get_variable_value(env3, "x");
	Object* var51 = get_variable_value(env3, "y");
	Object* var52_args[] = {var48, var49, var50, var51};
	Object* var52 = clisp_add(4, var52_args);

	Object* var53_args[] = {var52};
	Object* var53 = clisp_display(1, var53_args);
	destroy(var53);

	destroy(var52);
	destroy(var47);
	destroy(var46);
	destroy(var45);
	destroy(var44);
	destroy(var43);
	destroy(var38);
	destroy(var37);
	destroy_environment(env3);

	Environment* env4 = make_environment(env1, 1);
	Object* var54 = make_int(1);
	set_variable_value(env4, "u", var54);

	Environment* env5 = make_environment(env4, 1);
	Object* var55 = get_variable_value(env5, "u");
	set_variable_value(env5, "v", var55);

	Object* var56 = make_int(5);
	Object* var57 = update_variable_value(env5, "u", var56);

	Object* var58 = make_int(90);
	Object* var59 = update_variable_value(env5, "v", var58);

	Object* var60 = get_variable_value(env5, "u");
	Object* var61 = get_variable_value(env5, "v");
	Object* var62_args[] = {var60, var61};
	Object* var62 = clisp_add(2, var62_args);

	Object* var63_args[] = {var62};
	Object* var63 = clisp_display(1, var63_args);

	Object* var64_args[] = {var63};
	Object* var64 = clisp_display(1, var64_args);
	destroy(var64);

	destroy(var63);

	destroy(var62);
	destroy(var59);
	destroy(var58);
	destroy(var57);
	destroy(var56);
	destroy_environment(env5);
	destroy(var54);
	destroy_environment(env4);

	destroy(var14);
	destroy(var8);
	destroy(var4);
	destroy_environment(env1);

	return 0;
}
