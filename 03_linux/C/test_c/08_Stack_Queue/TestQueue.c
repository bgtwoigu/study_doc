/*
 * TestQueue.c
 *
 *  Created on: 2016年2月25日
 *      Author: xumingtao
 */

#include "CycleQueue.h"

int main() {
	SeQueue Q;
	int data = 3, value;

	//0. Init
	InitQueue(Q);
	PrintQueue(Q);

	//1. Enter Queue
	printf("\n");
	PrintQueue(Q);
	printf("EnQueue = %d\n", data);
	EnQueue(Q, data);
	PrintQueue(Q);

	//2. DeQueue
	printf("\n");
	PrintQueue(Q);
	value = Front(Q);
	DeQueue(Q);
	printf("DeQueue value = %d\n", value);
	PrintQueue(Q);

	//3. Clear
	printf("\n");
	PrintQueue(Q);
	printf("Clear Queue\n");
	ClearQueue(Q);
	PrintQueue(Q);

	return 0;
}
