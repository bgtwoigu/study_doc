#include"BiTree.h"
#include<malloc.h>
#include<stdlib.h>

/*构造一棵新的二叉树*/
BiTree InitBiTree(BiTNode *root) {
	BiTree tree = root;
	return tree;
}

/*生成节点*/
BiTNode *MakeNode(Item item, BiTNode *lchild, BiTNode *rchild) {
	BiTNode * pnode = (BiTNode *) malloc(sizeof(BiTNode));
	if (pnode) {
		pnode->data = item;
		pnode->lchild = lchild;
		pnode->rchild = rchild;
	}
	return pnode;
}

/*释放节点*/
void FreeNode(BiTNode *pnode) {
	if (pnode != NULL)
		free(pnode);
}

/*清空一棵二叉树*/
void ClearBiTree(BiTree tree) {
	BiTNode * pnode = tree;
	if (pnode->lchild != NULL)
		ClearBiTree(pnode->lchild);

	if (pnode->rchild != NULL)
		ClearBiTree(pnode->rchild);

	FreeNode(pnode);
}

/*销毁一棵二叉树*/
void DestroyBiTree(BiTree tree) {
	if (tree)
		ClearBiTree(tree);
}

/*判定是否为空*/
int IsEmpty(BiTree tree) {
	if (tree == NULL)
		return 0;
	else
		return 1;
}

/*返回树的深度*/
int GetDepth(BiTree tree) {
	int cd, ld, rd;
	cd = ld = rd = 0;
	if (tree) {
		ld = GetDepth(tree->lchild);
		rd = GetDepth(tree->rchild);
		cd = (ld > rd ? ld : rd);
		return cd + 1;
	} else
		return 0;
}

/*返回根*/
BiTree GetRoot(BiTree tree) {
	return tree;
}

/*返回节点值*/
Item GetItem(BiTNode *pnode) {
	return pnode->data;
}

/*设置节点值*/
void SetItem(BiTNode *pnode, Item item) {
	pnode->data = item;
}

/*设置左子树*/
BiTree SetLChild(BiTree parent, BiTree lchild) {
	parent->lchild = lchild;
	return lchild;
}

/*设置右子树*/
BiTree SetRChild(BiTree parent, BiTree rchild) {
	parent->rchild = rchild;
	return rchild;
}

/*返回左子树*/
BiTree GetLChild(BiTree tree) {
	if (tree)
		return tree->lchild;
	return NULL;
}

/*返回右子树*/
BiTree GetRChild(BiTree tree) {
	if (tree)
		return tree->rchild;
	return NULL;
}

/*插入新子树*/
BiTree InsertChild(BiTree parent, int lr, BiTree child) {
	if (parent) {
		if (lr == 0 && parent->lchild == NULL) {
			parent->lchild = child;
			return child;
		}
		if (lr == 1 && parent->rchild == NULL) {
			parent->rchild = child;
			return child;
		}
	}
	return NULL;
}

/*删除子树*/
void DeleteChild(BiTree parent, int lr) {
	if (parent) {
		if (lr == 0 && parent->lchild != NULL) {
			parent->lchild = NULL;
			FreeNode(parent->lchild);
		}
		if (lr == 1 && parent->rchild != NULL) {
			parent->rchild = NULL;
			FreeNode(parent->rchild);
		}
	}
}

/*先序遍历二叉树*/
void PreOrderTraverse(BiTree tree, void (*visit)(Item)) {
	BiTNode * pnode = tree;
	if (pnode) {
		visit(pnode->data);
		PreOrderTraverse(pnode->lchild, visit);
		PreOrderTraverse(pnode->rchild, visit);
	}
}

/*中序遍历二叉树*/
void InOrderTraverse(BiTree tree, void (*visit)(Item)) {
	BiTNode * pnode = tree;
	if (pnode) {
		InOrderTraverse(pnode->lchild, visit);
		visit(pnode->data);
		InOrderTraverse(pnode->rchild, visit);
	}
}

/*后序遍历二叉树*/
void PostOrderTraverse(BiTree tree, void (*visit)(Item)) {
	BiTNode * pnode = tree;
	if (pnode) {
		PostOrderTraverse(pnode->lchild, visit);
		PostOrderTraverse(pnode->rchild, visit);
		visit(pnode->data);
	}
}

/* 竖向打印二叉树 */
void printtree(BiTree tree, int nLayer) {
	int i = 0;
	BiTNode * pnode = tree;
	if (!pnode)
		return;
	printtree(pnode->lchild, nLayer + 3);
	for (i = 0; i < nLayer; i++)
		printf(" ");
	printf("%d\n", pnode->data);
	printtree(pnode->rchild, nLayer + 3);
}

