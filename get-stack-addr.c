/* This script prints its stack address during runtime for test purposes. */

#include <stdio.h>

void getStackAddr(void) {
        int stack_addr = 0;

        __asm__ (
                "movl %%esp, %0"
                : "=rm" (stack_addr)
        );

        printf("ESP: %X\n", stack_addr);
}

int main(void) {
        getStackAddr();
        return 0;
}
