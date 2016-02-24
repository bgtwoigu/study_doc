#include "LinkList.h"
#include <stdio.h>
#include <stdlib.h>

/* Create */
LinkList Create_List(int array[]) {
	LinkList L;
	NODE *p, *node;
	int i = 0;

	if (!array) {
		printf("Create List, array is null!\n");
		return NULL;
	}

	L = p = (NODE*) malloc(sizeof(NODE));
	if (!p) {
		printf("Create error!\n");
		return NULL;
	}

	p->data = array[0];
	p->link = NULL;
	//L = &p;
	i++;

	while (i < LINK_LENGTH) {
		node = (NODE*) malloc(sizeof(NODE));
		if (!node) {
			printf("Create error!\n");
			return NULL;
		}
		node->data = array[i];
		node->link = NULL;
		p->link = node;
		p = node;
		i++;
	}

	return L;
}

/* Free */
void Free_List(LinkList L) {
	NODE *node;
	while (L) {
		node = L;
		L = L->link;
		free(node);
	}
}

/* Insert */
int Insert_List(LinkList L, int k, int newElem) {
	int result = -1;
	NODE *node, *pre, *next;
	LinkList p = L;
	int length = getLength(p);

	if (p == NULL || p->link == NULL)
		return result;

	node = (NODE*) malloc(sizeof(NODE));
	node->data = newElem;
	node->link = NULL;

	printf("Insert node k = %d\n", k);
	if (k <= 1) {
		node->link = p;
		L = node;
	} else if (k >= length) {
		pre = Find_List(p, length);
		pre->link = node;
	} else {
		pre = Find_List(p, k);
		next = Find_List(p, k + 1);
		pre->link = node;
		node->link = next;
	}
	result = 0;

	return result;
}

/* Delete */
int Delete_List(LinkList L, int k) {
	int result = -1;
	LinkList p = L;
	NODE *pre, *next;
	int length = getLength(p);

	if (p == NULL || p->link == NULL)
		return result;

	printf("Delete node k = %d\n", k);
	if (k <= 1) {
		p = p->link;
		L = p;
	} else if (k >= length) {
		pre = Find_List(p, length - 1);
		pre->link = NULL;
	} else {
		pre = Find_List(p, k - 1);
		next = Find_List(p, k + 1);
		pre->link = next;
	}
	result = 0;

	return result;
}

/* Update */
int Update_List(LinkList L, int k, int updateElem) {
	int result = -1;
	NODE *node = Find_List(L, k);

	if (node) {
		node->data = updateElem;
		result = 0;
	}

	return result;
}

/* Find */
NODE* Find_List(LinkList L, int k) {
	LinkList p = L->link;
	int i = 1;

	while (p && i < k) {
		p = p->link;
		i++;
	}

	if (p && i == k) {
		printf("Find_List, k = %d\n", k);
		//Print_NODE(p);
		return p;
	}

	printf("Find_List, NULL, k = %d\n", k);
	return NULL;
}

int getLength(LinkList L) {
	int length = 0;
	LinkList p = L;

	while (p) {
		length++;
		p = p->link;
	}

	return length;
}

void Print_List(LinkList L) {
	LinkList p = L;
//	int *i;
//	char *c;
//	printf("siezof linklist = %0lx \n", sizeof(LinkList));
//	printf("siezof node = %0lx \n", sizeof(NODE));
//	printf("siezof int = %0lx \n", sizeof(int));
//	printf("siezof int* = %0lx \n", sizeof(&i));
//	printf("siezof char = %0lx \n", sizeof(char));
//	printf("siezof char* = %0lx \n", sizeof(&c));

	printf("List is: ");
	while (p) {
		printf("%d ", p->data);
		p = p->link;
	}

	printf("\n");
}

void Print_NODE(NODE* node) {
	if (node) {
		printf("Node is: data=%d\n", node->data);
	} else {
		printf("Node is null\n");
	}
}
