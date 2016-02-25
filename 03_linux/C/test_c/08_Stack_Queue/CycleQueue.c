/*
 * CycleQueue.c
 *
 *  Created on: 2016年2月25日
 *      Author: xumingtao
 */
#include "CycleQueue.h"

void InitQueue(SeQueue Q) {
	SeQueue q = Q;
	int i = 0;

	if (INITQSIZE > MAXQSIZE) {
		printf("Init Queue failed!\n");
		return;
	}

	srand((unsigned) time(NULL));
	q->base = (int*) malloc(MAXQSIZE * sizeof(int));
	q->front = q->rear = q->count = 0;
	while (i < INITQSIZE) {
		q->base[i] = rand() % 10 + 1;
		i++;
		q->count++;
	}

	q->rear = i % MAXQSIZE;

	printf("Init Queue!\n");
}

int Empty(SeQueue Q) {
	return (Q->count == 0);
}

int EnQueue(SeQueue Q, int data) {
	SeQueue q = Q;

	if (!q->base) {
		printf("EnQueue, Queue is NULL\n");
	}

	if (q->count >= MAXQSIZE) {
		printf("EnQueue, Queue is Full!\n");
		return -1;
	}

	q->base[q->rear] = data;
	q->rear = (q->rear + 1) % MAXQSIZE;
	q->count++;
	return 0;
}

int DeQueue(SeQueue Q) {
	SeQueue q = Q;

	if (!q->base) {
		printf("DeQueue, Queue is NULL\n");
	}

	if (q->count <= 0) {
		printf("DeQueue, **Queue is NULL!**\n");
		return -1;
	}

	q->base[q->front] = 0;
	q->front = (q->front + 1) % MAXQSIZE;
	q->count--;
	return 0;
}

int Front(SeQueue Q) {
	return Q->base[Q->front];
}

void ClearQueue(SeQueue Q) {
	Q->front = Q->rear = Q->count = 0;
	free(Q->base);
	Q->base = NULL;
}

void PrintQueue(SeQueue Q) {
	SeQueue q = Q;
	int i = 0;

	printf("Queue is: ");
	if (!q->base) {
		printf("\n");
		return;
	}

	while (i < MAXQSIZE) {
		printf("%d ", q->base[i]);
		i++;
	}

	printf("front = %d, rear = %d, count = %d\n", q->front, q->rear, q->count);
}
