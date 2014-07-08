#include "test.h"
#include <stdio.h>

int add(int a, int b)
{
    return a + b;
}

int main()
{
    printf(" 3 + 2 = %d\n", add(3, 2));
    printf(" 3 - 2 = %d\n", sub(3, 2));
    return 1;
}

