#include"BiTree.h"
#include<stdio.h>
void print(Item item) {
	printf("%d ", item);
}
main() {
	BiTNode * n1 = MakeNode(10, NULL, NULL);
	BiTNode * n2 = MakeNode(20, NULL, NULL);
	BiTNode * n3 = MakeNode(30, n1, n2);
	BiTNode * n4 = MakeNode(40, NULL, NULL);
	BiTNode * n5 = MakeNode(50, NULL, NULL);
	BiTNode * n6 = MakeNode(60, n4, n5);
	BiTNode * n7 = MakeNode(70, NULL, NULL);

	BiTree tree = InitBiTree(n7);
	SetLChild(tree, n3);
	SetRChild(tree, n6);

	printf("树的深度为：%d \n", GetDepth(tree));
	printtree(tree, GetDepth(tree));

	printf("\n先序遍历如下：");
	PreOrderTraverse(tree, print);

	printf("\n中序遍历如下：");
	InOrderTraverse(tree, print);

	printf("\n后序遍历如下：");
	PostOrderTraverse(tree, print);

	DeleteChild(tree, 1);
	printf("\n后序遍历如下：");
	PostOrderTraverse(tree, print);

	DestroyBiTree(tree);
	if (IsEmpty(tree))
		printf("\n二叉树为空，销毁完毕\n");
}
