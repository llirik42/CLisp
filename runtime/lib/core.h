#pragma once

enum ObjectType {
    INTEGER,
    DOUBLE,
    BOOLEAN,
    EVALUABLE,
    STRING,
    CHAR,
    UNSPECIFIED,
};

char* get_object_type_name(enum ObjectType type);

typedef struct {
    enum ObjectType type;
    unsigned short ref_count;
} Object;

#define CLISP_FUNC_PARAMS unsigned int count, Object** args
#define CLISP_FUNC_PARAMS_WITHOUT_TYPES count, args

enum ObjectType get_object_type(Object* obj);

void init_object(Object* obj, enum ObjectType type);

void increase_refs_count(Object* obj);

Object* clisp_make_unspecified();

void destroy_object(Object* obj);

unsigned char is_numeric(enum ObjectType type);
