### 一、介绍
通过把 **关键码值key映射到表中一个位置（数组的下标）** 来访问记录，以加快查找的速度。这个映射函数叫做散列函数，存放记录的数组叫做散列表，即哈希表。哈希表是一种典型的“以空间换时间”的做法。

- **键（key）：** 组员的编号
- **值（value）：** 组员的其他信息（值大小、姓名、年龄等）
- **索引：** 数组的下标，用以快速定位和检索数据
- **哈希桶：** 保存索引的数组（链表或数组），数组成员为每一个索引值相同的多个元素
- **哈希函数：** 将组员编号映射到索引，采用求余法（mod）
![Hash](https://img2024.cnblogs.com/blog/3775135/202603/3775135-20260309132107424-978632139.png)
红色方框即为5个哈希桶

### 二、代码
```cpp
/*=============== 链表实现 ===============*/
#include <iostream>
using namespace std;

#define DEFAULT_SIZE 16 // 哈希表默认大小

/*----- value节点 -----*/
struct Node
{
    Node *next;  // 下一个值
    int key;     // 键，此处使用int类型作为key，也可以是char、string……
    void *value; // 值，使用void*以达到可以存储不同类型的值的效果（泛型）
};

/*----- 哈希表 -----*/
struct HashTable
{
    int TableSize;  // 哈希表的大小（桶的数量）
    Node *Thelists; // 哈希桶数组（每个元素是一个链表的头节点）
};

/*----- 哈希函数 -----*/
int Hash(int key, int TableSize)
{
    return key % TableSize;
}

/*----- 初始化哈希表 -----*/
HashTable *initHashTable(int size = DEFAULT_SIZE)
{
    HashTable *ht = new HashTable;
    ht->TableSize = size;
    ht->Thelists = new Node[size];

    // 初始化每个桶的链表头节点
    for (int i = 0; i < size; i++)
    {
        ht->Thelists[i].next  = NULL;
        ht->Thelists[i].key   = -1;
        ht->Thelists[i].value = NULL;
    }
    return ht;
}

/*----- 插入键值对 -----*/
void insert(HashTable *ht, int key, void *value)
{
    int index = Hash(key, ht->TableSize);

    // 创建新节点
    Node *newNode = new Node;
    newNode->key = key;
    newNode->value = value;

    // 插入到链表头部
    newNode->next = ht->Thelists[index].next;
    ht->Thelists[index].next = newNode;
}

/*----- 查找值 -----*/
void *search(HashTable *ht, int key)
{
    int index = Hash(key, ht->TableSize);

    Node *cur = ht->Thelists[index].next;
    while (cur != NULL)
    {
        if (cur->key == key) return cur->value;
        cur = cur->next;
    }
    return NULL;
}

/*----- 删除键值对 -----*/
bool remove(HashTable *ht, int key)
{
    int index = Hash(key, ht->TableSize);

    Node *pre = &ht->Thelists[index];
    Node *cur = pre->next;

    while (cur != NULL)
    {
        if (cur->key == key)
        {
            pre->next = cur->next;
            delete cur;
            return true;
        }
        pre = cur;
        cur = cur->next;
    }
    return false;
}

/*----- 销毁哈希表 -----*/
void destroy(HashTable *ht)
{
    for (int i = 0; i < ht->TableSize; i++)
    {
        Node *cur = ht->Thelists[i].next;
        while (cur != NULL)
        {
            Node *tmp = cur;
            cur = cur->next;
            delete tmp;
        }
    }
    delete[] ht->Thelists;
    delete ht;
}

int main()
{
    HashTable *ht = initHashTable(); // 创建并初始化哈希表

    /*--- 插入 ---*/
    int value1 = 100;
    char value2 = 'A'; // 使用void*的好处，可以存储其他的类型
    int value3 = 300;
    insert(ht, 1, &value1);
    insert(ht, 11, &value2); // 会产生冲突，11%10=1
    insert(ht, 2, &value3);

    /*--- 查找数据 ---*/
    int* result1 = (int*)search(ht, 1);
    if (result1 != nullptr) cout << "找到键1对应的值: " << *result1 << endl;

    char *result2 = (char*)search(ht, 11);
    if (result2 != nullptr) cout << "找到键11对应的值: " << *result2 << endl;

    /*--- 删除数据 ---*/
    if (remove(ht, 1)) cout << "成功删除键1！" << endl;

    /*--- 再次查找已被删除的数据 ---*/
    result1 = (int*)search(ht, 1);
    if (result1 == nullptr) cout << "键1已被删除，找不到对应值" << endl;

    /*--- 销毁哈希表 ---*/
    destroy(ht);
    cout << "哈希表已被销毁！" << endl;

    return 0;
}
```