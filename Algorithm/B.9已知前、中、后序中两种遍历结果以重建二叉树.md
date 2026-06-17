
当知道前序遍历、中序遍历、后序遍历中的两种遍历方式，就能够反推出二叉树的结构了。
但是要注意一点：已知**前序遍历&后序遍历**结果时，**二叉树不能有节点的度为1！！！**
**提醒：** 此处默认二叉树节点存储的值为int类型，其他类型，如char等可以将vector换为string等
**例题：**[遍历问题](https://www.luogu.com.cn/problem/P1229)，[美国血统](https://www.luogu.com.cn/problem/P1827)

### 一、已知前&中序遍历结果
```cpp
// 对应洛谷：https://www.luogu.com.cn/problem/P1827
#include <iostream>
#include <unordered_map>
#include <vector>
using namespace std;

struct Node
{
    int val;
    Node *l, *r;

    Node(int x) : val(x), l(nullptr), r(nullptr) {}
};

class BinaryTreeBuilder
{
private:
    unordered_map<int, int> inorderMap; // 存储中序遍历中各元素的索引位置
    int preorderIndex;                  // 前序遍历的当前索引

public:
    // 主函数，依据中序与前序遍历构建二叉树
    Node* buildTree(vector<int>& preorder, vector<int>& inorder)
    {
        for (int i = 0; i < (int)inorder.size(); i++) inorderMap[inorder[i]] = i;
        preorderIndex = 0;
        return buildHelper(preorder, 0, inorder.size()-1);
    }

private:
    // 递归辅助函数
    Node* buildHelper(vector<int>& preorder, int inorderStart, int inorderEnd)
    {
        if (inorderStart > inorderEnd) return NULL;
        // 前序遍历的当前元素即为根节点
        int rootVal = preorder[preorderIndex++];
        Node *root = new Node(rootVal);
        // 在中序遍历中找到根节点的位置
        int rootIdx = inorderMap[rootVal];
        // 构建左、右子树（递归）
        root->l = buildHelper(preorder, inorderStart, rootIdx-1); // 中序遍历中在根节点前的都属于左子树
        root->r = buildHelper(preorder, rootIdx+1, inorderEnd);   // 在后面的是右子树部分

        return root;
    }

public:
    // 销毁树
    void destroyTree(Node *root)
    {
        if (root == NULL) return;
        destroyTree(root->l);
        destroyTree(root->r);
        delete root;
    }

    // 中序遍历验证（左-根-右）
    void inOrder(Node *root)
    {
        if (root == NULL) return;
        inOrder(root->l);
        cout << root->val << " ";
        inOrder(root->r);
    }
    
    // 前序遍历验证（根-左-右）
    void preOrder(Node *root)
    {
        if (root == NULL) return;
        cout << root->val << " ";
        preOrder(root->l);
        preOrder(root->r);
    }
    
    // 后序遍历（左-右-根）
    void postOrder(Node *root)
    {
        if (root == NULL) return;
        postOrder(root->l);
        postOrder(root->r);
        cout << root->val << " ";
    }
};

int main()
{
    // 示例：根据给定的中序和前序遍历构建二叉树
    vector<int> preorder = {3, 9, 20, 15, 7};  // 前序遍历结果
    vector<int> inorder = {9, 3, 15, 20, 7};   // 中序遍历结果
    
    BinaryTreeBuilder builder;
    Node* root = builder.buildTree(preorder, inorder);
    
    cout << "构建的二叉树遍历结果：" << endl;
    cout << "前序遍历: ";
    builder.preOrder(root);
    cout << endl;
    
    cout << "中序遍历: ";
    builder.inOrder(root);
    cout << endl;
    
    cout << "后序遍历: ";
    builder.postOrder(root);
    cout << endl;

    builder.destroyTree(root);
    root = NULL;
    cout << "二叉树销毁完毕！" << endl;
    return 0;
}
```

### 二、已知前&后序遍历结果
**注意：二叉树不能有节点的度为1！！！**
[遍历问题](https://www.luogu.com.cn/problem/P1229)这道题是*已知前、后序遍历求有多少种中序遍历结果*，中序遍历中度等于1的节点是影响结果的因素，这个也是为什么在[已知前、中、后序中两种遍历结果以重建二叉树](https://shu-jvan.github.io/2025/12/08/%EF%BC%882%EF%BC%89%E5%B7%B2%E7%9F%A5%E5%89%8D%E3%80%81%E4%B8%AD%E3%80%81%E5%90%8E%E5%BA%8F%E4%B8%AD%E4%B8%A4%E7%A7%8D%E9%81%8D%E5%8E%86%E7%BB%93%E6%9E%9C%E4%BB%A5%E9%87%8D%E5%BB%BA%E4%BA%8C%E5%8F%89%E6%A0%91/)中设置度不等于1。看了题解知道了一个知识点：*前序中出现AB，后序中出现BA，则这个节点只有一个儿子*。而这样的话只要找个度为1的节点数n，那么结果就是*pow(2, n+1)*。但是我们答题的时候一般使用*找AB, BA*的方法，使用*substr(i, 2)截取AB，reverse得到BA，再find*。
```cpp
// 后序遍历的最后一个元素是根节点
// 但是这要求不能有度为1的节点（这不就是哈夫曼树嘛）
/*
解决方法：
1. 前序遍历的第一个元素是树的根节点
2. 后序遍历的最后一个元素也是树的根节点
3. 前序遍历中根节点之后的第一个元素通常是左子树的根节点（如果存在左子树）
4. 在后序遍历中找到这个左子树根节点的位置，就可以划分左右子树的范围
*/
#include <iostream>
#include <unordered_map>
#include <vector>
using namespace std;

struct Node
{
    int val;
    Node *l, *r;

    Node(int x) : val(x), l(nullptr), r(nullptr) {}
};

class BuildTree
{
private:
    unordered_map<int, int> postorderMap;
    int preorderIndex;

public:
    Node *build(vector<int> preorder, vector<int> postorder)
    {
        for (int i = 0; i < (int)postorder.size(); i++) postorderMap[postorder[i]] = i;
        preorderIndex = 0;
        return buildHelper(preorder, 0, postorder.size()-1);
    }

private:
    Node *buildHelper(vector<int> preorder, int postStart, int postEnd)
    {
        if (postStart > postEnd || preorderIndex >= (int)preorder.size()) return NULL;

        int rootVal = preorder[preorderIndex++];
        Node *root = new Node(rootVal);

        if (postStart == postEnd) return root; // 只有一个节点，则直接返回

        // 在后序遍历中找到左子树根节点的位置
        int lRootVal = preorder[preorderIndex];
        int lRootIdx = postorderMap[lRootVal];

        root->l = buildHelper(preorder, postStart, lRootIdx);
        root->r = buildHelper(preorder, lRootIdx+1, postEnd-1);

        return root;
    }

public:
    // 销毁树
    void destroyTree(Node *root)
    {
        if (root == NULL) return;
        destroyTree(root->l);
        destroyTree(root->r);
        delete root;
    }

    // 中序遍历验证（左-根-右）
    void inOrder(Node *root)
    {
        if (root == NULL) return;
        inOrder(root->l);
        cout << root->val << " ";
        inOrder(root->r);
    }
    
    // 前序遍历验证（根-左-右）
    void preOrder(Node *root)
    {
        if (root == NULL) return;
        cout << root->val << " ";
        preOrder(root->l);
        preOrder(root->r);
    }
    
    // 后序遍历（左-右-根）
    void postOrder(Node *root)
    {
        if (root == NULL) return;
        postOrder(root->l);
        postOrder(root->r);
        cout << root->val << " ";
    }
};

int main()
{
    // 示例：根据给定的前序和后序遍历构建二叉树
    vector<int> preorder = {1, 2, 4, 5, 3, 6, 7};   // 前序遍历结果
    vector<int> postorder = {4, 5, 2, 6, 7, 3, 1};  // 后序遍历结果
    
    BuildTree builder;
    Node* root = builder.build(preorder, postorder);
    
    cout << "根据前序和后序遍历重建的二叉树：" << endl;
    cout << "前序遍历: ";
    builder.preOrder(root);
    cout << endl;
    
    cout << "中序遍历: ";
    builder.inOrder(root);
    cout << endl;
    
    cout << "后序遍历: ";
    builder.postOrder(root);
    cout << endl;
    
    // 释放内存
    builder.destroyTree(root);
    root = nullptr;
    
    cout << "二叉树内存已释放！" << endl;

    return 0;
}
```

### 三、已知中&后序遍历结果
```cpp
// 这个和已知前&中差不多，因为只要找到根节点——后序遍历的最后一个元素，再将中序遍历中左右子树（根节点的前后）递归创建拼接即可
#include <iostream>
#include <unordered_map>
#include <vector>
using namespace std;

struct Node
{
    int val;
    Node *l, *r;

    Node(int x) : val(x), l(nullptr), r(nullptr) {}
};

class Tree
{
private:
    unordered_map<int, int> inorderMap;
    int postorderIndex;

public:
    Node *build(vector<int> inorder, vector<int> postorder)
    {
        for (int i = 0; i < (int)inorder.size(); i++) inorderMap[inorder[i]] = i;
        postorderIndex = postorder.size() - 1;
        return buildHelper(postorder, 0, inorder.size()-1);
    }

private:
    Node *buildHelper(vector<int> postorder, int inorderStart, int inorderEnd)
    {
        if (inorderStart > inorderEnd) return NULL;

        int rootVal = postorder[postorderIndex--];
        Node *root = new Node(rootVal);

        int rootIdx = inorderMap[rootVal];

        root->r = buildHelper(postorder, rootIdx+1, inorderEnd);
        root->l = buildHelper(postorder, inorderStart, rootIdx-1);

        return root;
    }

public:
    // 销毁树
    void destroyTree(Node *root)
    {
        if (root == NULL) return;
        destroyTree(root->l);
        destroyTree(root->r);
        delete root;
    }

    // 中序遍历验证（左-根-右）
    void inOrder(Node *root)
    {
        if (root == NULL) return;
        inOrder(root->l);
        cout << root->val << " ";
        inOrder(root->r);
    }
    
    // 前序遍历验证（根-左-右）
    void preOrder(Node *root)
    {
        if (root == NULL) return;
        cout << root->val << " ";
        preOrder(root->l);
        preOrder(root->r);
    }
    
    // 后序遍历（左-右-根）
    void postOrder(Node *root)
    {
        if (root == NULL) return;
        postOrder(root->l);
        postOrder(root->r);
        cout << root->val << " ";
    }
};

int main()
{
    // 示例：根据给定的中序和前序遍历构建二叉树
    vector<int> preorder = {9, 3, 15, 20, 7};  // 中序遍历结果
    vector<int> inorder = {9, 15, 7, 20, 3};   // 后序遍历结果
    
    Tree builder;
    Node* root = builder.build(preorder, inorder);
    
    cout << "构建的二叉树遍历结果：" << endl;
    cout << "前序遍历: ";
    builder.preOrder(root);
    cout << endl;
    
    cout << "中序遍历: ";
    builder.inOrder(root);
    cout << endl;
    
    cout << "后序遍历: ";
    builder.postOrder(root);
    cout << endl;

    builder.destroyTree(root);
    root = NULL;
    cout << "二叉树销毁完毕！" << endl;

    return 0;
}
```