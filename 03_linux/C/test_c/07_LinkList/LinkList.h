#ifndef _LINKLIST_H_
#define _LINKLIST_H_

typedef struct node {
	int data;
	struct node *link;
} NODE, *LinkList;

#define LINK_LENGTH 10

/* Create */
LinkList Create_List(int array[]);

/* Free */
void Free_List(LinkList L);

/* Insert */
int Insert_List(LinkList L, int k, int newElem);

/* Delete */
int Delete_List(LinkList L, int k);

/* Update */
int Update_List(LinkList L, int k, int updateElem);

/* Find */
NODE* Find_List(LinkList L, int k);

/* length */
int getLength(LinkList L);

/* Print List*/
void Print_List(LinkList L);

/* Print Node */
void Print_NODE(NODE* node);
#endif
