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

void print(Object* obj);

#endif
