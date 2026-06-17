
### 一、介绍
类比浏览器的搜索功能，近期搜索的内容会在搜索记录的最上方，而之前的则相对较为下面，这就是伸展树的原理：**将上一次Search的节点通过一系列AVL树的旋转操作变为树的根**。

### 二、伸展操作
从底向上沿着访问路径旋转，令node为访问路径上的一个"非根节点"
1. 若node的父节点是根节点，那么只要旋转node和根，这是沿着访问路径上最后的旋转
2. node有父节点和祖父节点，此时有两种情况：
  1）"之"字形：执行一次AVL树的双旋转
  2）"一"字形：将高度|子 < 父 < 爷| --> |爷 < 父 < 子|
"之"就是子是父的左（右）子节点，父是爷的右（左）；"一"就是父&子同为左/右子节点

---
**伸展代码**
```cpp
// 伸展操作，把node伸展上去
void splay(Node *&root, Node *node)
{
    while (node->p != NULL)
    {
        if (node->p->p == NULL) // 父节点是根，即没有祖父节点
        {
            // 父节点是根节点，单旋转
            if (node->p->l == node) rightRotate(root, node->p); // Zig
            else leftRotate(root, node->p);  // Zag
        } else // 有祖父节点
        {
            Node *parent = node->p;
            Node *grandparent = parent->p;
            
            if (parent->l == node && grandparent->l == parent)
            {
                // Zig-Zig
                rightRotate(root, grandparent);
                rightRotate(root, parent);
            } else if (parent->r == node && grandparent->r == parent)
            {
                // Zag-Zag
                leftRotate(root, grandparent);
                leftRotate(root, parent);
            } else if (parent->r == node && grandparent->l == parent)
            {
                // Zig-Zag
                leftRotate(root, parent);
                rightRotate(root, grandparent);
            } else
            {
                // Zag-Zig
                rightRotate(root, parent);
                leftRotate(root, grandparent);
            }
        }
    }
}
```

### 三、测试代码
**C++**
```cpp
#include <iostream>
#include <string>
#include <queue> // 层次遍历用
using namespace std;

struct Node
{
    string Name;
    Node *l, *r, *p;
    Node(string s) : Name(s), l(NULL), r(NULL), p(NULL) {}
};

// 函数声明
Node* search(Node *&root, string s);    // 查找（查找后进行伸展）
void insert(Node *&root, string s);     // 插入
void deleteNode(Node *&root, string s); // 删除
void splay(Node *&root, Node *node);    // 伸展：自底向上
void leftRotate(Node *&root, Node *x);  // 左旋
void rightRotate(Node *&root, Node *x); // 右旋
void printTree(Node *root);             // 打印
void destroyTree(Node *root);           // 销毁

// 左旋操作，将y移到上面去
void leftRotate(Node *&root, Node *x)
{
    Node *y = x->r;
    if (y == NULL) return;
    
    x->r = y->l;
    if (y->l != NULL) y->l->p = x;
    
    y->p = x->p;
    
    if (x->p == NULL) root = y;
    else if (x == x->p->l) x->p->l = y;
    else x->p->r = y;
    
    y->l = x;
    x->p = y;
}

// 右旋操作，将x移到上面去
void rightRotate(Node *&root, Node *x)
{
    Node *y = x->l;
    if (y == NULL) return;
    
    x->l = y->r;
    if (y->r != NULL) y->r->p = x;
    
    y->p = x->p;
    
    if (x->p == NULL) root = y;
    else if (x == x->p->r) x->p->r = y;
    else x->p->l = y;
    
    y->r = x;
    x->p = y;
}

// 伸展操作，把node伸展上去
void splay(Node *&root, Node *node)
{
    while (node->p != NULL)
    {
        if (node->p->p == NULL) // 父节点是根，即没有祖父节点
        {
            // 父节点是根节点，单旋转
            if (node->p->l == node) rightRotate(root, node->p); // Zig
            else leftRotate(root, node->p);  // Zag
        } else // 有祖父节点
        {
            Node *parent = node->p;
            Node *grandparent = parent->p;
            
            if (parent->l == node && grandparent->l == parent)
            {
                // Zig-Zig
                rightRotate(root, grandparent);
                rightRotate(root, parent);
            } else if (parent->r == node && grandparent->r == parent)
            {
                // Zag-Zag
                leftRotate(root, grandparent);
                leftRotate(root, parent);
            } else if (parent->r == node && grandparent->l == parent)
            {
                // Zig-Zag
                leftRotate(root, parent);
                rightRotate(root, grandparent);
            } else
            {
                // Zag-Zig
                rightRotate(root, parent);
                leftRotate(root, grandparent);
            }
        }
    }
}

// 搜索操作
Node* search(Node *&root, string s)
{
    if (root == NULL) return NULL;
    
    Node *current = root;
    Node *last = NULL;
    bool found = false;
    
    while (current != NULL)
    {
        last = current;
        if (s < current->Name) current = current->l;
        else if (s > current->Name) current = current->r;
        else
        {
            found = true;
            break;
        }
    }
    
    // 伸展最后一个访问的节点
    if (found)
    {
        splay(root, last); // 伸展找到的节点
        return last;
    }
    else if (last != NULL)
    {
        splay(root, last); // 伸展最后一个访问的节点
        return NULL;       // 未找到
    }
    
    return NULL;
}

// 插入操作
void insert(Node *&root, string s)
{
    Node *newNode = new Node(s);
    
    if (root == NULL)
    {
        root = newNode;
        return;
    }
    
    Node *current = root;
    Node *parent = NULL;
    
    while (current != NULL)
    {
        parent = current;
        if (s < current->Name) current = current->l;
        else if (s > current->Name) current = current->r;
        else
        {
            // 重复插入，删除新节点并返回
            delete newNode;
            return;
        }
    }
    
    // 插入新节点
    newNode->p = parent;
    if (s < parent->Name) parent->l = newNode;
    else parent->r = newNode;
    
    // 伸展新插入的节点到根
    splay(root, newNode);
}

// 删除操作
void deleteNode(Node *&root, string s)
{
    if (root == NULL) return;
    
    // 搜索要删除的节点（会自动伸展）
    Node *nodeToDelete = search(root, s);
    if (nodeToDelete == NULL || nodeToDelete->Name != s)
    {
        cout << "查无此点！" << endl;
        return;
    }
    
    // 现在要删除的节点是根节点
    Node *leftTree = root->l;
    Node *rightTree = root->r;
    
    // 删除根节点
    delete root;
    
    if (leftTree == NULL)
    {
        root = rightTree;
        if (root != NULL) root->p = NULL;
    } else if (rightTree == NULL)
    {
        root = leftTree;
        if (root != NULL) root->p = NULL;
    } else
    {
        // 两个子树都存在
        // 找到左子树的最大节点
        Node *maxInLeft = leftTree;
        while (maxInLeft->r != NULL) maxInLeft = maxInLeft->r;
        
        // 将左子树的最大节点伸展到左子树的根
        splay(leftTree, maxInLeft);
        
        // 连接右子树
        maxInLeft->r = rightTree;
        rightTree->p = maxInLeft;
        
        root = maxInLeft;
        root->p = NULL;
    }
}

// 层次遍历
void levelOrder(Node *root)
{
    if (root == NULL) return;
    
    queue<Node*> q;
    q.push(root);
    
    while (!q.empty())
    {
        Node *current = q.front();
        q.pop();
        cout << current->Name << " ";
        
        if (current->l != NULL) q.push(current->l);
        if (current->r != NULL) q.push(current->r);
    }
}

// 先序遍历
void preOrder(Node *root)
{
    if (root == NULL) return;
    cout << root->Name << " ";
    preOrder(root->l);
    preOrder(root->r);
}

// 中序遍历
void inOrder(Node *root)
{
    if (root == NULL) return;
    inOrder(root->l);
    cout << root->Name << " ";
    inOrder(root->r);
}

// 后序遍历
void postOrder(Node *root)
{
    if (root == NULL) return;
    postOrder(root->l);
    postOrder(root->r);
    cout << root->Name << " ";
}

// 打印树
void printTree(Node *root)
{
    if (root == NULL)
    {
        cout << "树是空的！" << endl;
        return;
    }
    
    cout << "层次遍历：";
    levelOrder(root);
    cout << endl << endl;
}

// 销毁树
void destroyTree(Node *root)
{
    if (root == NULL) return;
    destroyTree(root->l);
    destroyTree(root->r);
    delete root;
}

// 主函数
int main()
{
    Node *root = NULL;

    // 测试插入
    insert(root, "apple");
    insert(root, "banana");
    insert(root, "cherry");
    insert(root, "date");
    
    cout << "初始插入后：" << endl;
    printTree(root);

    // 测试搜索（会自动伸展）
    Node *result = search(root, "banana");
    if (result != NULL && result->Name == "banana")
    {
        cout << "查找 banana 后：" << endl;
        printTree(root);
    }

    // 测试删除
    deleteNode(root, "cherry");
    cout << "删除 cherry 后：" << endl;
    printTree(root);

    // 清理
    destroyTree(root);
    root = NULL;
    
    cout << "摧毁树后：" << endl;
    printTree(root);
    
    return 0;
}
```

**C语言**
```c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

// 以学号Id排序
typedef struct Node
{
    int Grade;
    char *Major;
    int Class;
    char *Name;
    int Id;
    struct Node *l, *r, *p;
} Node;

// 函数声明
Node* createNode(int grade, char *major, int Class, char *name, int id); // 创建新节点
Node* search(Node *root, int id);          // 查找（查找后进行伸展）
Node* insert(Node *root, char *name);      // 插入（非递归实现）
Node* deleteNode(Node *root, int id);      // 删除
Node* splay(Node *root, Node *node);       // 伸展：自底向上
Node* leftRotate(Node *root, Node *x);     // 左旋
Node* rightRotate(Node *root, Node *y);    // 右旋
void printTree(Node *root);                // 打印
void destroyTree(Node *root);              // 销毁

Node* createNode(int grade, char *major, int Class, char *name, int id)
{
    Node* newNode = (Node*)malloc(sizeof(Node));
    newNode->Grade = grade;
    newNode->Major = (char*)malloc(sizeof(char) * (strlen(major) + 1));
    strcpy(newNode->Major, major);
    newNode->Class = Class;
    newNode->Name = (char*)malloc(sizeof(char) * (strlen(name) + 1));
    strcpy(newNode->Name, name);
    newNode->Id = id;
    newNode->l = newNode->r = newNode->p = NULL;

    return newNode;
}

Node* search(Node *root, int id)
{
    if (root == NULL) return NULL;
    Node *curr = root, *last = NULL; // 当前访问与最后访问的节点
    while (curr != NULL)
    {
        last = curr;
        if (id < curr->Id) curr = curr->l;
        else if (id > curr->Id) curr = curr->r;
        else return splay(root, curr); // 找到节点，进行伸展
    }

    if (last != NULL) return splay(root, last); // 未找到节点，则伸展最后访问的

    return root;
}

Node* insert(Node *root, char *name)
{
    printf("Please enter %s's grade, major, class and id: ", name);
    printf("\n");
    int grade, Class, id;
    char major[100];
    scanf("%d %s %d %d", &grade, major, &Class, &id);
    Node *newNode = createNode(grade, major, Class, name, id);

    if (root == NULL)
    {
        root = newNode;
        return root;
    }

    Node *current = root, *parent = NULL;
    while (current != NULL)
    {
        parent = current;
        if (id < current->Id) current = current->l;
        else if (id > current->Id) current = current->r;
        else
        {
            printf("Student %s is already exist!\n", name);
            free(newNode->Major);
            free(newNode->Name);
            free(newNode);
            return root;
        }
    }

    newNode->p = parent;
    if (id < parent->Id) parent->l = newNode;
    else parent->r = newNode;

    return root;
}

// 删除辅助函数
Node *findMin(Node *root)
{
    if (root == NULL) return NULL;
    while (root->l != NULL) root = root->l;
    return root;
}

Node* deleteNode(Node *root, int id)
{
    if (root == NULL) return NULL;
    if (id < root->Id) root->l = deleteNode(root->l, id);
    else if (id > root->Id) root->r = deleteNode(root->r, id);
    else
    {
        if (root->l == NULL && root->r == NULL) // leaf node
        {
            free(root->Major);
            free(root->Name);
            free(root);
            return NULL;
        } else if (root->l == NULL) // only exists right child node
        {
            Node *tmp = root->r;
            free(root->Major);
            free(root->Name);
            free(root);
            return tmp;
        } else if (root->r == NULL) // only exists left child node
        {
            Node *tmp = root->l;
            free(root->Major);
            free(root->Name);
            free(root);
            return tmp;
        } else // both left child and right child exist
        {
            Node *succ = findMin(root->r);
            root->Grade = succ->Grade;
            free(root->Major);
            root->Major = (char*)malloc(sizeof(char) * (strlen(succ->Major) + 1));
            strcpy(root->Major, succ->Major);
            root->Class = succ->Class;
            free(root->Name);
            root->Name = (char*)malloc(sizeof(char) * (strlen(succ->Name) + 1));
            strcpy(root->Name, succ->Name);
            root->Id = succ->Id;

            root->r = deleteNode(root->r, succ->Id);
        }
    }
    return root;
}

Node* splay(Node *root, Node *node)
{
    if (node == NULL || node == root) return root;
    
    while (node->p != NULL) // till node become the root
    {
        Node *parent = node->p;
        Node *grandparent = parent->p;

        if (grandparent == NULL) // only exists parent node, doesn't exist grandpa node
        {
            if (node == parent->l) root = rightRotate(root, parent);
            else root = leftRotate(root, parent);
        } else
        {
            if (parent->l == node && grandparent->l == parent) // Zig-Zig
            {
                root = rightRotate(root, grandparent);
                root = rightRotate(root, parent);
            } else if (parent->r == node && grandparent->r == parent) // Zag-Zag
            {
                root = leftRotate(root, grandparent);
                root = leftRotate(root, parent);
            } else if (parent->l == node && grandparent->r == parent) // Zag-Zig
            {
                root = rightRotate(root, parent);
                root = leftRotate(root, grandparent);
            } else // Zig-Zag
            {
                root = leftRotate(root, parent);
                root = rightRotate(root, grandparent);
            }
        }
    }
    return root;
}

Node* leftRotate(Node *root, Node *x)
{
    if (x == NULL || x->r == NULL) return root;
    
    Node *y = x->r;
    x->r = y->l;
    if (y->l != NULL) y->l->p = x;

    y->p = x->p;
    if (x->p == NULL) root = y;
    else if (x == x->p->l) x->p->l = y;
    else x->p->r = y;

    y->l = x;
    x->p = y;

    return root;
}

Node* rightRotate(Node *root, Node *y)
{
    if (y == NULL || y->l == NULL) return root;
    
    Node *x = y->l;
    y->l = x->r;
    if (x->r != NULL) x->r->p = y;

    x->p = y->p;
    if (y->p == NULL) root = x;
    else if (y == y->p->l) y->p->l = x;
    else y->p->r = x;

    x->r = y;
    y->p = x;

    return root;
}

void printTree(Node *root)
{
    if (root == NULL)
    {
        printf("SplayTree is empty!\n");
        return;
    }

    Node* queue[127];
    int front = 0, rear = 0;
    queue[rear++] = root;
    while (front < rear)
    {
        Node *cur = queue[front++];
        printf("Grade: %d, Major: %s, Class: %d, Name: %s, Id: %d\n", cur->Grade, cur->Major, cur->Class, cur->Name, cur->Id);

        if (cur->l) queue[rear++] = cur->l;
        if (cur->r) queue[rear++] = cur->r;
    }
    printf("\n");
}

void destroyTree(Node *root)
{
    if (root == NULL) return;
    destroyTree(root->l);
    destroyTree(root->r);
    free(root->Major);
    free(root->Name);
    free(root);
}

int main()
{
    Node *root = NULL;

    // test data
    char s1[] = "Alice";
    char s2[] = "Bob";
    char s3[] = "Charlie";
    char s4[] = "Avril";
    char s5[] = "Taylor";
    char s6[] = "Luna";

    root = insert(root, s1);
    root = insert(root, s2);
    root = insert(root, s3);
    root = insert(root, s4);
    root = insert(root, s5);
    root = insert(root, s6);
    
    printf("After insert students:\n");
    printTree(root);
    
    // test the search function
    root = search(root, 2);
    printf("search the student who's Id is 2:\n");
    printTree(root);
    
    // test the delete function
    root = deleteNode(root, 2);
    printf("delete the student who's id is 2:\n");
    printTree(root);
    
    // destroy splaytree
    destroyTree(root);
    return 0;
}
```