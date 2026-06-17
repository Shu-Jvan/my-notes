
### 一、介绍

1. **作用:** 平衡二叉树的精髓就在于平衡。对于普通的**BST**，若节点多的话，就很容易出现**左右不协调**的问题，即左边很高，右边很矮，或者相反，从而导致**search**过程很慢，而平衡二叉树**可以让左右子树的高度差在1范围内**，这样就可以避免左右不协调的问题，加快search速度。

2. **核心:** abs(Height(left_child_tree) - Height(right_child_tree)) <= 1，即左右子树高度差不能超过1

3. **旋转示意图:**
- **左单旋转**
![lRotate](https://img2024.cnblogs.com/blog/3775135/202603/3775135-20260309132558985-1964673308.png)

- **右单旋转**
![rRotate](https://img2024.cnblogs.com/blog/3775135/202603/3775135-20260309132638733-685881632.png)

- **左右双旋转**
![lrRotate](https://img2024.cnblogs.com/blog/3775135/202603/3775135-20260309132709767-623954229.png)

### 二、代码
**结构体:**
```C
typedef struct Node
{
    int value;
    struct Node *l, *r;
    int height;
} Node;
```

**左旋:**
```C
Node *leftRotate(Node *x)
{
    Node *y = x->r; // 右边为y
    Node *t = y->l; // 把y的左子树变为x的右子树
    // 旋转
    y->l = x;
    x->r = t;
    // 更新高度
    x->height = max(getHeight(x->l), getHeight(x->r)) + 1;
    y->height = max(getHeight(y->l), getHeight(y->r)) + 1;
    // 返回新根节点y
    return y;
}
```

**右旋:**
```C
Node *rightRotate(Node *y)
{
    Node *x = y->l; // 左边为x
    Node *t = x->r; // 把x的右子树变为y的左子树
    // 旋转
    x->r = y;
    y->l = t;
    // 更新高度
    x->height = max(getHeight(x->l), getHeight(x->r)) + 1;
    y->height = max(getHeight(y->l), getHeight(y->r)) + 1;
    // 返回新根节点x
    return x;
}
```

### 三、测试代码

**C语言版:**
```C
#include <stdio.h>
#include <stdlib.h>

typedef struct Node
{
    int value;
    struct Node *l, *r;
    int height;
} Node;

/*===== 老演员 =====*/
Node *create(int n);
Node *find(Node *root, int n);
Node *findMin(Node *root);
Node *insert(Node *root, int n);
Node *deleteNode(Node *root, int n);
void destroyTree(Node *root);
void levelOrder(Node *root);
void preOrder(Node *root);
void inOrder(Node *root);
void postOrder(Node *root);
void print(Node *root);
/*===== 主角 =====*/
int max(int a, int b);      // 辅助函数
int getHeight(Node* node);  // 获取节点高度
int getBalance(Node* node); // 获取平衡因子
Node *leftRotate(Node *x);  // 左旋，x、y表示相对位置，左边为x，右边为y
Node *rightRotate(Node *y); // 右旋

//========================================================================//

Node *create(int n)
{
    Node *newNode = (Node*)malloc(sizeof(Node)); // C语言中可以不用类型转换(Node*)，C++中要，但是C++有new，不用malloc了
    newNode->value = n;
    newNode->l = newNode->r = NULL;
    newNode->height = 1;
    return newNode;
}

Node *find(Node *root, int n)
{
    if (root == NULL) return NULL;
    if (n < root->value) return find(root->l, n);
    else if (n > root->value) return find(root->r, n);
    return root;
}

Node *findMin(Node *root)
{
    while (root && root->l) root = root->l;
    return root;
}

Node *insert(Node *root, int n)
{
    // 正常执行BST插入
    if (root == NULL) return create(n);
    if (n < root->value) root->l = insert(root->l, n);
    else if (n > root->value) root->r = insert(root->r, n);
    else return root;
    // 更新祖先节点的高度
    root->height = max(getHeight(root->l), getHeight(root->r)) + 1;
    // 获取平衡因子
    int balance = getBalance(root);
    // 平衡过程
    if (balance > 1 && n < root->l->value) return rightRotate(root); // 左子树高，且插入的n到了左子树里面，右单旋
    if (balance < -1 && n > root->r->value) return leftRotate(root); // 右子树高，且插入的n到了右子树里面，左单旋
    if (balance > 1 && n > root->l->value) // 左子树高，且插入的n到了右子树里面，左右双旋
    {
        root->l = leftRotate(root->l);
        return rightRotate(root);
    }
    if (balance < -1 && n < root->r->value) // 右子树高，且插入的n到了左子树里面，右左双旋
    {
        root->r = rightRotate(root->r);
        return leftRotate(root);
    }

    return root; // 返回未改变的节点指针
}

Node *deleteNode(Node *root, int n)
{
    // 正常执行BST删除
    if (root == NULL) return NULL;
    if (n < root->value) root->l = deleteNode(root->l, n);
    else if (n > root->value) root->r = deleteNode(root->r, n);
    else
    {
        if (root->l == NULL && root->r == NULL) // 叶节点
        {
            free(root);
            return NULL;
        } else if (root->r == NULL) // 只存在左子树
        {
            Node *tmp = root->l;
            free(root);
            return tmp; // 返回左子树，让if中的 root->l = tmp
        } else if (root->l == NULL) // 只存在右子树
        {
            Node *tmp = root->r;
            free(root);
            return tmp;
        } else
        {
            Node *tmp = findMin(root->r); // 找到右子树的最小值对应的节点
            root->value = tmp->value;
            root->r = deleteNode(root->r, tmp->value); // 删除右子树的最小值对应的节点
        }
    }

    // 更新高度
    root->height = max(getHeight(root->l), getHeight(root->r)) + 1;
    // 获取平衡因子
    int balance = getBalance(root);

    // 旋转
    if (balance > 1 && getBalance(root->l) >= 0) return rightRotate(root); // 左子树、左子树的左子树高，右单旋
    if (balance < -1 && getBalance(root->r) <= 0) return leftRotate(root); // 右子树、右子树的右子树高，左单旋
    if (balance > 1 && getBalance(root->l) < 0) // 左子树高，但是左子树的右子树高，左右双旋
    {
        root->l = leftRotate(root->l);
        return rightRotate(root);
    }
    if (balance < -1 && getBalance(root->r) > 0) // 右子树高，但是右子树的左子树高，右左双旋
    {
        root->r = rightRotate(root->r);
        return leftRotate(root);
    }

    return root;
}

void destroyTree(Node *root)
{
    if (root == NULL) return;
    destroyTree(root->l);
    destroyTree(root->r);
    free(root);
}

void levelOrder(Node *root)
{
    if (root == NULL) return;
    Node *queue[127];        // 假设最多有127个节点（其实也可以是无限个，只要循环使用数组就可以了，不过这样很麻烦）
    int front = 0, rear = 0; // 队头、队尾
    queue[rear++] = root;    // 根节点入队

    while (front < rear)
    {
        Node *cur = queue[front++];
        printf("%d ", cur->value);

        if (cur->l != NULL) queue[rear++] = cur->l;
        if (cur->r != NULL) queue[rear++] = cur->r;
    }
}

void preOrder(Node *root)
{
    if (root == NULL) return;
    printf("%d ", root->value);
    preOrder(root->l);
    preOrder(root->r);
}

void inOrder(Node *root)
{
    if (root == NULL) return;
    inOrder(root->l);
    printf("%d ", root->value);
    inOrder(root->r);
}

void postOrder(Node *root)
{
    if (root == NULL) return;
    postOrder(root->l);
    postOrder(root->r);
    printf("%d ", root->value);
}

void print(Node *root)
{
    if (root == NULL)
    {
        printf("树为空！\n");
        return;
    }

    printf("层次遍历：");
    levelOrder(root);
    printf("\n");

    printf("先序遍历：");
    preOrder(root);
    printf("\n");

    printf("中序遍历：");
    inOrder(root);
    printf("\n");

    printf("后序遍历：");
    postOrder(root);
    printf("\n\n");
}

int getHeight(Node* node)
{
    if (node == NULL) return 0;
    return node->height;
}

int getBalance(Node* node)
{
    if (node == NULL) return 0;
    return getHeight(node->l) - getHeight(node->r);
}

int max(int a, int b)
{
    return a > b ? a : b;
}

Node *leftRotate(Node *x)
{
    Node *y = x->r; // 右边为y
    Node *t = y->l; // 把y的左子树变为x的右子树
    // 旋转
    y->l = x;
    x->r = t;
    // 更新高度
    x->height = max(getHeight(x->l), getHeight(x->r)) + 1;
    y->height = max(getHeight(y->l), getHeight(y->r)) + 1;
    // 返回新根节点y
    return y;
}

Node *rightRotate(Node *y)
{
    Node *x = y->l; // 左边为x
    Node *t = x->r; // 把x的右子树变为y的左子树
    // 旋转
    x->r = y;
    y->l = t;
    // 更新高度
    x->height = max(getHeight(x->l), getHeight(x->r)) + 1;
    y->height = max(getHeight(y->l), getHeight(y->r)) + 1;
    // 返回新根节点x
    return x;
}

int main()
{
    Node* root = NULL;
    root = insert(root, 10);
    root = insert(root, 20);
    print(root);
    root = insert(root, 30);
    // 不平衡了
    print(root);
    root = insert(root, 40);
    root = insert(root, 50);
    root = insert(root, 25);
    print(root);

    printf("删除30后:\n");
    root = deleteNode(root, 30);
    print(root);

    destroyTree(root);
    root = NULL;
    printf("树已被销毁！\n");
    print(root);

    return 0;
}
```

**C++版**
```cpp
#include <iostream>
#include <queue>
#include <algorithm>
using namespace std;

struct Node
{
    int value;
    Node *l, *r;
    int height;
};

/*===== 老演员 =====*/
Node *Create(int n);
Node *Find(Node *root, int n);
Node *findMin(Node *root);
Node *Insert(Node *root, int n);
Node *Delete(Node *root, int n);
void destroyTree(Node *root);
void LeOT(Node *root);
void PrOT(Node *root);
void InOT(Node *root);
void PoOT(Node *root);
void Print(Node *root);
/*===== 主角 =====*/
int getHeight(Node* node);  // 获取节点高度
int getBalance(Node* node); // 获取平衡因子
Node *leftRotate(Node *x);  // 左旋，x、y表示相对位置，左边为x，右边为y
Node *rightRotate(Node *y); // 右旋

int main()
{
    Node* root = nullptr;
    
    // 测试插入
    root = Insert(root, 10);
    root = Insert(root, 20);
    root = Insert(root, 30);
    root = Insert(root, 40);
    root = Insert(root, 50);
    root = Insert(root, 25);
    
    cout << "AVL树构建完成：" << endl;
    Print(root);
    
    // 测试删除
    root = Delete(root, 30);
    cout << "\n删除节点30后：";
    Print(root);
    
    destroyTree(root);
    return 0;
}

Node *Create(int n)
{
    Node *newNode = new Node;
    newNode->value = n;
    newNode->l = newNode->r = nullptr;
    newNode->height = 1;
    return newNode;
}

Node *Find(Node *root, int n)
{
    if (root == nullptr) return nullptr;
    if (n < root->value) return Find(root->l, n);
    else if (n > root->value) return Find(root->r, n);
    return root;
}

Node *findMin(Node *root)
{
    while (root && root->l) root = root->l;
    return root;
}

Node *Insert(Node *root, int n)
{
    /*--- 执行正常的BST插入 ---*/
    if (root == nullptr) return Create(n);
    if (n < root->value) root->l = Insert(root->l, n);
    else if (n > root->value) root->r = Insert(root->r, n);
    else return root; // AVL树中没有值相等的节点，直接返回自身节点

    /*--- 更新祖先节点的高度 ---*/
    root->height = max(getHeight(root->l), getHeight(root->r)) + 1;

    /*--- 获取平衡因子 ---*/
    int balance = getBalance(root);

    /*--- 若插入后变得不平衡 ---*/
    if (balance > 1 && n < root->l->value) return rightRotate(root); // 左子树高，且插入的n到了左子树里面，右单旋
    if (balance < -1 && n > root->r->value) return leftRotate(root); // 右子树高，且插入的n到了右子树里面，左单旋
    if (balance > 1 && n > root->l->value) // 左子树高，且插入的n到了右子树里面，左右双旋
    {
        root->l = leftRotate(root->l);
        return rightRotate(root);
    }
    if (balance < -1 && n < root->r->value) // 右子树高，且插入的n到了左子树里面，右左双旋
    {
        root->r = rightRotate(root->r);
        return leftRotate(root);
    }

    return root; // 返回未改变的节点指针
}

Node *Delete(Node *root, int n)
{
    /*--- 执行正常的BST删除 ---*/
    if (root == nullptr) return nullptr;

    if (n < root->value) root->l = Delete(root->l, n);
    else if (n > root->value) root->r = Delete(root->r, n);
    else
    {
        if (root->l == nullptr && root->r == nullptr) // leaf node
        {
            delete root;
            return nullptr;
        } else if (root->l == nullptr) // only exist right child tree
        {
            Node *tmp = root->r;
            delete root;
            return tmp;
        } else if (root->r == nullptr) // only exist left child tree
        {
            Node *tmp = root->l;
            delete root;
            return tmp;
        } else // left & right both exist
        {
            Node *tmp = findMin(root->r);
            root->value = tmp->value;
            root->r = Delete(root->r, tmp->value);
        }
    }
    if (root == nullptr) return root; // 若传入的树只有一个节点，则直接返回

    /*--- 更新高度 ---*/
    root->height = max(getHeight(root->l), getHeight(root->r)) + 1;

    /*--- 获取平衡因子 ---*/
    int balance = getBalance(root);

    /*--- 若删除后节点变得不平衡 ---*/
    if (balance > 1 && getBalance(root->l) >= 0) return rightRotate(root); // 左子树、左子树的左子树高，右单旋
    if (balance < -1 && getBalance(root->r) <= 0) return leftRotate(root); // 右子树、右子树的右子树高，左单旋
    if (balance > 1 && getBalance(root->l) < 0) // 左子树高，但是左子树的右子树高，左右双旋
    {
        root->l = leftRotate(root->l);
        return rightRotate(root);
    }
    if (balance < -1 && getBalance(root->r) > 0) // 右子树高，但是右子树的左子树高，右左双旋
    {
        root->r = rightRotate(root->r);
        return leftRotate(root);
    }

    return root;
}

void destroyTree(Node *root)
{
    if (root == nullptr) return;
    destroyTree(root->l);
    destroyTree(root->r);
    delete root;
}

void LeOT(Node *root)
{
    if (root == nullptr) return;

    queue<Node*> q;
    q.push(root);
    while (!q.empty())
    {
        Node *cur = q.front(); q.pop();
        cout << cur->value << " ";
        if (cur->l) q.push(cur->l);
        if (cur->r) q.push(cur->r);
    }
}

void PrOT(Node *root)
{
    if (root == nullptr) return;
    cout << root->value << " ";
    PrOT(root->l);
    PrOT(root->r);
}

void InOT(Node *root)
{
    if (root == nullptr) return;
    InOT(root->l);
    cout << root->value << " ";
    InOT(root->r);
}

void PoOT(Node *root)
{
    if (root == nullptr) return;
    PoOT(root->l);
    PoOT(root->r);
    cout << root->value << " ";
}

void Print(Node *root)
{
    if (root == nullptr)
    {
        cout << "AVLTree is empty!" << endl;
        return;
    }

    cout << endl << "------------------------------" << endl;
    cout << "层次遍历：";
    LeOT(root);

    cout << endl << "------------------------------" << endl;
    cout << "先序遍历：";
    PrOT(root);

    cout << endl << "------------------------------" << endl;
    cout << "中序遍历：";
    InOT(root);

    cout << endl << "------------------------------" << endl;
    cout << "后序遍历：";
    PoOT(root);

    cout << endl << "------------------------------" << endl;
    cout << "输出完毕！" << endl;
}

int getHeight(Node* node)
{
    if (node == nullptr) return 0;
    return node->height;
}

int getBalance(Node* node)
{
    if (node == nullptr) return 0;
    return getHeight(node->l) - getHeight(node->r);
}

Node *leftRotate(Node *x)
{
    Node *y = x->r;
    Node *T2 = y->l;

    /*--- 执行旋转 ---*/
    y->l = x;
    x->r = T2;

    /*--- 更新高度 ---*/
    x->height = max(getHeight(x->l), getHeight(x->r)) + 1;
    y->height = max(getHeight(y->l), getHeight(y->r)) + 1;

    return y; // 返回新的根节点
}

Node *rightRotate(Node *y)
{
    Node *x = y->l;
    Node *T2 = x->r;

    /*--- 执行旋转 ---*/
    x->r = y;
    y->l = T2;

    /*--- 更新高度 ---*/
    y->height = max(getHeight(y->l), getHeight(y->r)) + 1;
    x->height = max(getHeight(x->l), getHeight(x->r)) + 1;

    return x;
}
```