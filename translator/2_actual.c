#include "runtime.h"

int main() {
	Environment* env1 = make_environment(NULL, 0);
	
	Environment* env2 = make_environment(env1, 1);
	Object* var1 = make_int(1);
	set_variable_value(env2, "a", var1);
	
	Object* var2 = get_variable_value(env2, "a");
	Object* var3 = make_int(2);
	Object* var4_args[] = {var2, var3};
	Object* var4 = clisp_add(2, var4_args);
	
	Environment* env3 = make_environment(env1, 1);
	Object* var5 = make_int(4);
	set_variable_value(env3, "a", var5);
	
	Object* var6 = make_int(3);
	Object* var7 = get_variable_value(env3, "a");
	Object* var8_args[] = {var6, var7};
	Object* var8 = clisp_mul(2, var8_args);
	
	Object* var9_args[] = {var4, var8};
	Object* var9 = clisp_add(2, var9_args);
	Object* var10_args[] = {var9};
	Object* var10 = clisp_display(1, var10_args);
	destroy(var10);
	destroy(var9);
	
	destroy(var8);
	destroy(var6);
	destroy(var5);
	destroy_environment(env3);
	
	destroy(var4);
	destroy(var3);
	destroy(var1);
	destroy_environment(env2);
	
	destroy_environment(env1);
	
	return 0;
}
