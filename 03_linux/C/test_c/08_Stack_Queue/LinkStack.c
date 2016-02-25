/*
 * LinkStack.c
 *
 *  Created on: 2016年2月25日
 *      Author: xumingtao
 */
#include "LinkStack.h"

int InitStack(LinkStack S) {
	pNode node, nextNode;
	LinkStack p = S;
	int i = 1;

	p->bottom = p->top = NULL;

	srand((unsigned) time(NULL));
	while (i <= INIT_STACK_SIZE) {
		node = (pNode) malloc(sizeof(Node));
		if (!node) {
			printf("Init Stack, Create Node failed\n");
			return -1;
		}
		node->data = rand() % 100 + 1;
		node->pNext = NULL;
		if (i == 1) {
			p->bottom = node;
		} else {
			nextNode->pNext = node;
		}

		if (i == INIT_STACK_SIZE)
			p->top = node;

		nextNode = node;
		i++;
	}

	printf("Init Stack OK!\n");
	return 0;
}

int StackEmpty(LinkStack S) {
	LinkStack p = S;
	if (!p || !p->top)
		return 1;

	return 0;
}

int Push(LinkStack S, pNode node) {
	LinkStack p = S;
	pNode topNode;

	if (p) {
		topNode = p->top;
		topNode->pNext = node;
		p->top = node;
	} else {
		p->top = node;
		p->bottom = node;
	}
	return 0;
}

int Pop(LinkStack S) {
	LinkStack p = S;
	pNode preNode, topNode;
	int i = 0;
	int length = lengthStack(p);

	if (!p) {
		printf("Stack NULL\n");
		return -1;
	}

	preNode = FindStack(p, length - 1);
	if (preNode) {
		preNode->pNext = NULL;
	}

	topNode = p->top;
	if (topNode) {
		free(topNode);
	}

	return 0;
}

pNode Top(LinkStack S) {
	LinkStack p = S;
	pNode node;

	if (!p) {
		printf("Stack NULL\n");
		return NULL;
	}

	node = p->top;

	return node;
}

int ClearStack(LinkStack S) {
	LinkStack p = S;
	pNode node, next;

	if (!p) {
		printf("Stack NULL\n");
		return -1;
	}

	next = p->bottom;
	if (!next) {
		printf("Stack NULL, Node NuLL\n");
		return -1;
	}

	while (next->pNext) {
		node = next;
		next = next->pNext;
		node->pNext = NULL;
		node->data = 0;
		free(node);
	}

	free(next);
	p->top = p->bottom = NULL;

	return 0;
}

int lengthStack(LinkStack S) {
	LinkStack p = S;
	pNode node;
	int length = 0;

	if (!p)
		return 0;

	node = p->bottom;

	if (!node) {
		return 0;
	} else if (!node->pNext) {
		return 1;
	} else {
		length++;
		while (node->pNext) {
			node = node->pNext;
			length++;
		}
	}

	printf("Stack length = %d\n", length);
	return length;
}

pNode FindStack(LinkStack S, int k) {
	LinkStack p = S;
	pNode node;
	int length = lengthStack(p);
	int i = 1;

	if (!p) {
		printf("Stack NULL\n");
		return NULL;
	}

	node = p->bottom;
	if (k <= 1) {
		node = p->bottom;
	} else if (k >= length) {
		node = p->top;
	} else {
		i++;
		while (i <= k) {
			node = node->pNext;
			i++;
		}
	}

	return node;
}

void PrintStack(LinkStack S) {
	LinkStack p = S;
	pNode node;

	if (!p) {
		printf("Print Stack, NULL\n");
		return;
	}

	printf("Stack is: ");
	node = p->bottom;
	while (node) {
		printf("%d ", node->data);
		node = node->pNext;
	}
	printf("\n");
}

void PrintNode(pNode node) {
	if (!node) {
		printf("Node is NULL\n");
		return;
	}

	printf("Node data = %d\n", node->data);
}

pNode CreateNode(int data) {
	pNode node;

	node = (pNode) malloc(sizeof(Node));
	if (!node) {
		printf("Create Node failed\n");
		return NULL;
	}
	node->data = data;
	node->pNext = NULL;
	return node;
}
