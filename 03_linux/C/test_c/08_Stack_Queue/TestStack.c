/*
 * TestStack.c
 *
 *  Created on: 2016年2月25日
 *      Author: xumingtao
 */

#include "LinkStack.h"

int main() {
	LinkStack S;
	int result;
	pNode node, topNode;

	//0. InitStack
	InitStack(S);
	if (!S) {
		printf("Init Stack failed!\n");
		return -1;
	}
	PrintStack(S);

	//1. Push
	printf("\n");
	PrintStack(S);
	printf("Push Stack\n");
	node = CreateNode(5);
	if (!node) {
		printf("Create Node failed\n");
		return -1;
	}
	Push(S, node);
	PrintStack(S);
	topNode = Top(S);
	PrintNode(topNode);

	//2. Pop
	printf("\n");
	PrintStack(S);
	if (!StackEmpty(S)) {
		printf("Pop Stack\n");
		Pop(S);
	}
	PrintStack(S);

	//3. Clear
	printf("\n");
	PrintStack(S);
	if (!StackEmpty(S)) {
		printf("Clear Stack\n");
		ClearStack(S);
	}
	PrintStack(S);
}
