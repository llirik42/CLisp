#include "objects/lambda.h"

#include "lib/memory.h"

Object* clisp_make_lambda(clisp_func_with_env func, Environment* environment) {
    LambdaObject* lambda_object = allocate_memory(sizeof(LambdaObject));
    init_object((Object*)lambda_object, LAMBDA);

    lambda_object->func.clisp_func_with_env = func;
    lambda_object->with_env = TRUE;
    lambda_object->environment = environment;
    return (Object*)lambda_object;
}

Object* clisp_make_lambda_without_env(clisp_func func) {
    LambdaObject* lambda_object = allocate_memory(sizeof(LambdaObject));
    init_object((Object*)lambda_object, LAMBDA);

    lambda_object->func.clisp_func = func;
    lambda_object->with_env = FALSE;
    return (Object*)lambda_object;
}

void destroy_lambda(Object* obj) {
    free_memory(obj);
}

Object* clisp_lambda_call(Object* obj, CLISP_FUNC_PARAMS) {
    const LambdaObject* lambda_object = (LambdaObject*)obj;
    if (lambda_object->with_env) {
        return lambda_object->func.clisp_func_with_env(lambda_object->environment, CLISP_FUNC_PARAMS_WITHOUT_TYPES);
    }
    return lambda_object->func.clisp_func(CLISP_FUNC_PARAMS_WITHOUT_TYPES);
}
