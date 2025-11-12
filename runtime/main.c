#include <stdarg.h>
#include <stdio.h>

// Variadic function to add numbers
int getSum(int n, ...) {
    int sum = 0;

    // Declaring a va_list pointer to
    // argument list
    va_list list;

    // Initializing argument to the
    // list pointer
    va_start(list, n);

    for (int i = 0; i < n; i++)

        // Accessing current variable
        // and pointing to next one
        sum += va_arg(list, int);

    // Ending argument list traversal
    va_end(list);

    return sum;
}


typedef struct {
    int numberOfArgs;
    int (*func)(int n, ...);

} MyStruct;

int main() {
    MyStruct s = {};

    s.numberOfArgs = 3;
    s.func = getSum;

    return 0;
}
