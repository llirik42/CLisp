#include "objects/lambda.h"

#include "lib/memory.h"

Object* clisp_make_lambda(lambda func, Environment* environment) {
    LambdaObject* lambda_object = allocate_memory(sizeof(LambdaObject));
    init_object((Object*)lambda_object, LAMBDA);

    lambda_object->func = func;
    lambda_object->environment = environment;
    return (Object*)lambda_object;
}

void destroy_lambda(Object* obj) {
    free_memory(obj);
}

Object* clisp_lambda_call(Object* obj, CLISP_FUNC_PARAMS) {
    const LambdaObject* lambda_object = (LambdaObject*)obj;
    return lambda_object->func(lambda_object->environment, count, args);
}
