/*
 * LinkStack.h
 *
 *  Created on: 2016年2月25日
 *      Author: xumingtao
 */

#ifndef LINKSTACK_H_
#define LINKSTACK_H_

#include <stdio.h>
#include <stdlib.h>

#define INIT_STACK_SIZE 5

typedef struct node{
	int data;
	struct node *pNext;
}Node, *pNode;

typedef struct linkstack{
	pNode top;
	pNode bottom;
}*LinkStack;

int InitStack(LinkStack S);
int StackEmpty(LinkStack S);
int Push(LinkStack S, pNode node);
int Pop(LinkStack S);
pNode Top(LinkStack S);
int ClearStack(LinkStack S);
int lengthStack(LinkStack S);
pNode FindStack(LinkStack S, int k);
void PrintStack(LinkStack S);
void PrintNode(pNode node);
pNode CreateNode(int data);

#endif /* LINKSTACK_H_ */
