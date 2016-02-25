/*
 * CycleQueue.h
 *
 *  Created on: 2016年2月25日
 *      Author: xumingtao
 */

#ifndef CYCLEQUEUE_H_
#define CYCLEQUEUE_H_

#include <stdio.h>
#include <stdlib.h>

#define MAXQSIZE 6
#define INITQSIZE 4

typedef struct {
	int *base;
	int front; // point front
	int rear; // point rear
	int count; //count of queue
}*SeQueue;

void InitQueue(SeQueue Q);
int Empty(SeQueue Q);
int EnQueue(SeQueue Q, int data);
int DeQueue(SeQueue Q);
int Front(SeQueue Q);
void ClearQueue(SeQueue Q);
void PrintQueue(SeQueue Q);

#endif /* CYCLEQUEUE_H_ */
