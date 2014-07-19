#include <stdio.h>
#include <time.h>
#include <sys/time.h>
#include <stdlib.h>
#include <signal.h>

static int count = 0;
static struct itimerval oldtv;
const int LOOP_NUMBER = 15;

void set_timer()
{
    struct itimerval itv;
    itv.it_interval.tv_sec = 1;
    itv.it_interval.tv_usec = 0;
    itv.it_value.tv_sec = 1;
    itv.it_value.tv_usec = 0;
    setitimer(ITIMER_REAL, &itv, &oldtv);
}

void signal_handler(int m)
{
    count++;
    printf("count = %d\n", count);
}

int main()
{
    signal(SIGALRM, signal_handler);
    set_timer();
    while(count < LOOP_NUMBER);
    exit(0);
    return 1;
}
