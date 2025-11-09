#ifndef RUNTIME
#define RUNTIME

enum ObjectType {
    INTEGER,
    DOUBLE,
    RATIO
};

typedef struct {
    void* value;
    enum ObjectType type;
} Object;

Object* make_int(int value);

void destroy(Object* obj);

// TODO:
Object* clisp_display(Object* obj);

// TODO:
Object* clisp_add(Object* a1, Object* a2);

#endif
