#define _POSIX_C_SOURCE 200809L
#include <stdlib.h>
#include <stdio.h>
#include <time.h>
#include <pthread.h>
#include <unistd.h>
#include <string.h>
#include "timespec_operations.h"
#include "eat.h"


#define NUM_THREADS 4

static struct timespec initial_time;

struct hilo_args {
    int idx; // índice del hilo
    struct timespec wait_time;
    struct timespec period;
};

struct hilo_args THREAD1 = {
    .wait_time = {0, 450000000}, 
    .idx = 0,
    .period =  {1, 400000000}
};
struct hilo_args THREAD2 = {
    .wait_time = {0, 900000000}, 
    .idx = 1,
    .period =  {2, 900000000}
};
struct hilo_args THREAD3 = {
    .wait_time = {3, 000000000}, 
    .idx = 2,
    .period =  {13, 000000000}
};
struct hilo_args THREAD4 = {
    .wait_time = {5, 600000000}, 
    .idx = 3,
    .period =  {50, 000000000}
};

struct timespec worst_times[NUM_THREADS];      //I will use this one to get and update the worst time of each thread

// Show a message with the relative elapsed time, and response_time
void report (char * message, int id, struct timespec *response_time) {
  struct timespec now;
  clock_gettime(CLOCK_MONOTONIC,&now);
  decr_timespec(&now,&initial_time);
  printf("%3.3f - %s - %d",(double) (now.tv_sec+
	 now.tv_nsec/1.0e9),message,id);
  if (response_time==NULL) {
    printf("\n");
  } else {
    printf(" - %3.3f\n",(double) (response_time->tv_sec+
				  response_time->tv_nsec/1.0e9));
  }
}

void *function(void *args){
    int err;
    struct hilo_args *datos = (struct hilo_args *)args;

    int puntero = datos->idx;
    struct timespec wait_time = datos->wait_time;
    struct timespec period_time = datos->period;
    struct timespec next_time;
    struct timespec response_time;


    clock_gettime(CLOCK_MONOTONIC, &next_time);
    while (1)
    {
        report ("Start thread ",puntero,NULL);
        action(puntero, wait_time);

        clock_gettime(CLOCK_MONOTONIC, &response_time);
        decr_timespec(&response_time,&next_time);
        report ("End   thread ",puntero,&response_time);
        
        if (smaller_timespec(&worst_times[puntero], &response_time)){
            worst_times[puntero] = response_time;
        }
        
        
        
        incr_timespec(&next_time, &period_time);
        err = clock_nanosleep(CLOCK_MONOTONIC, TIMER_ABSTIME, &next_time, NULL);
        if (err != 0) {
            printf("Error en clock_nanosleep: %s\n", strerror(err));
            pthread_exit(NULL);
        }
    }
    

    return NULL;
}

void action (int puntero, struct timespec wait_time){
    int err;

    struct timespec time_to_eat;
    struct timespec begin, end;

    //printf("Test for EAT function\n");

    time_to_eat.tv_sec = wait_time.tv_sec;
    time_to_eat.tv_nsec = wait_time.tv_nsec;
    err  =clock_gettime(CLOCK_THREAD_CPUTIME_ID, &begin);
    eat(&time_to_eat);
    err = clock_gettime(CLOCK_THREAD_CPUTIME_ID, &end);

    decr_timespec(&end, &begin);
    

}

// Main program that creates two periodic threads
int main ()
{
    pthread_t t[NUM_THREADS];
    struct hilo_args thread_args[] = {THREAD1,THREAD2, THREAD3, THREAD4};
    struct sched_param sch_param;
    
    pthread_attr_t attr;
    clock_gettime(CLOCK_MONOTONIC, &initial_time);
    //Desomentar despues
    // Set the priority of the main program to max_prio-1
    sch_param.sched_priority = 
    (sched_get_priority_max(SCHED_FIFO)-1); 
    if (pthread_setschedparam(pthread_self(),SCHED_FIFO,&sch_param) !=0)
    {
        printf("Error while setting main thread's priority\n");
        exit(1);
    }

    //I put the attibutes
    if (pthread_attr_init(&attr) != 0) {
        printf("Error en pthread_attr_init\n");
        exit(1);
    }
    if (pthread_attr_setinheritsched (&attr,PTHREAD_EXPLICIT_SCHED) != 0) 
    { 
        printf("Error in inheritsched attribute\n");
        exit(1);
    }
    if (pthread_attr_setdetachstate(&attr,PTHREAD_CREATE_DETACHED) != 0) {
        printf("Error en atributo detachstate\n");
        exit(1);
    }
    if (pthread_attr_setschedpolicy (&attr, SCHED_FIFO) != 0) {
        printf("Error en atributo schedpolicy\n");
        exit(1);
    }


    for(int i = 0; i < NUM_THREADS; i ++){
        worst_times[i].tv_nsec = 0;
        worst_times[i].tv_sec = 0;
        //I change the priorities
        sch_param.sched_priority = 
        (sched_get_priority_max(SCHED_FIFO)-2-i); 
        if (pthread_attr_setschedparam (&attr,&sch_param) != 0) 
        {
            printf("Error en atributo schedparam\n");
            exit(1);
        }
        if (pthread_create (&t[i],&attr,function,&thread_args[i]) != 0) {
            printf("Error en creacion de thread %i\n", i);
    }
    }

    

    while (1){
        sleep(5);  // Espera 5 segundos
        for (int i = 0; i < NUM_THREADS; i++) {
            report ("Peor Tiempo ",i,&worst_times[i]);
            
        }
    }
    
    exit(0);
}

