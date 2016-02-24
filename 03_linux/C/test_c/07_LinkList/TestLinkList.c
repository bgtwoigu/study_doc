#include "LinkList.h"
#include <stdio.h>
#include <stdlib.h>

int main() {
	int array[LINK_LENGTH] = { 1, 3, 4, 2, 9, 6, 7, 5, 0, 8 };
	LinkList L;
	int i = 0;
	NODE *node;

	printf("Array is: ");
	while (i < LINK_LENGTH) {
		printf("%d ", array[i]);
		i++;
	}
	printf("\n");

	//0. create
	printf("Create_List\n");
	L = Create_List(array);
	Print_List(L);

	//1. find
	printf("\n");
	printf("Find_List\n");
	Print_List(L);
	node = Find_List(L, 3);
	Print_NODE(node);

	//2. update
	printf("\n");
	Print_List(L);
	printf("Update_List\n");
	Update_List(L, 3, 23);
	Print_List(L);

	//3. insert
	printf("\n");
	Print_List(L);
	printf("Insert_List\n");
	Insert_List(L, 3, 99);
	Print_List(L);

	//4. delete
	printf("\n");
	Print_List(L);
	printf("Delete_List\n");
	Delete_List(L, 8);
	Print_List(L);

	//5. free
	printf("\n");
	Print_List(L);
	printf("Free resource!\n");
	Free_List(L);
	Print_List(L);
	return 0;
}
