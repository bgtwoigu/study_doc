typedef int Item;
typedef struct node {
	struct node * lchild;
	struct node * rchild;
	Item data;
} BiTNode, *BiTree;

/*构造一棵新的二叉树*/
BiTree InitBiTree(BiTNode *root);

/*生成节点*/
BiTNode *MakeNode(Item item, BiTNode *lchild, BiTNode *rchild);

/*释放节点*/
void FreeNode(BiTNode *pnode);

/*清空一棵二叉树*/
void ClearBiTree(BiTree tree);

/*销毁一棵二叉树*/
void DestroyBiTree(BiTree tree);

/*判定是否为空*/
int IsEmpty(BiTree tree);

/*返回树的深度*/
int GetDepth(BiTree tree);

/*返回根*/
BiTree GetRoot(BiTree tree);

/*返回节点值*/
Item GetItem(BiTNode *pnode);

/*设置节点值*/
void SetItem(BiTNode *pnode, Item item);

/*设置左子树*/
BiTree SetLChild(BiTree parent, BiTree lchild);

/*设置右子树*/
BiTree SetRChild(BiTree parent, BiTree rchild);

/*返回左子树*/
BiTree GetLChild(BiTree tree);

/*返回右子树*/
BiTree GetRChild(BiTree tree);

/*插入新子树*/
BiTree InsertChild(BiTree parent, int lr, BiTree child);

/*删除子树*/
void DeleteChild(BiTree parent, int lr);

/*先序遍历二叉树*/
void PreOrderTraverse(BiTree tree, void (*visit)());

/*中序遍历二叉树*/
void InOrderTraverse(BiTree tree, void (*visit)());

/*后序遍历二叉树*/
void PostOrderTraverse(BiTree tree, void (*visit)());

/* 竖向打印二叉树 */
void printtree(BiTree bt, int nLayer);
