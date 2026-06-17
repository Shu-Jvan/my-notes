### 一、说明
**优先队列**是一种特殊的队列，其中每个元素都有一个优先级。出队操作总是返回具有最高优先级的元素，而不是等待时间最长的元素。

### 二、特点
1. **有序性**：元素按照优先级排序，而不是按插入顺序
2. **动态性**：支持动态插入和删除操作
3. **高效性**：插入和删除操作的时间复杂度为O(log n)

### 三、实现原理
优先队列通常使用**堆**这种数据结构来实现。堆是一棵完全二叉树，满足堆性质：
- **最大堆（大根堆）**：父节点的值大于或等于其子节点的值
    > arr[i] >= arr[2*i+1] && arr[i] >= arr[2*i+2]
- **最小堆（小根堆）**：父节点的值小于或等于其子节点的值
    > arr[i] <= arr[2*i+1] && arr[i] <= arr[2*i+2]

### 四、堆的存储结构
堆通常使用数组来存储，对于索引为i的节点：
- 父节点索引：(i-1)/2
- 左子节点索引：2*i+1
- 右子节点索引：2*i+2

### 五、代码
1. **C++** 代码：
```cpp
#include <iostream>
#include <functional>
#include <stdlib.h>
#include <time.h>
using namespace std;

class PriorityQueue
{
public: // 构造与析构函数
    using Cmp = function<bool(int, int)>;
    PriorityQueue(Cmp cmp = greater<int>()) // greater表示大根堆
        : size_(0), cap_(20), cmp_(cmp)
        {
            que_ = new int[cap_];
        }

    ~PriorityQueue()
    {
        delete[] que_;
        que_ = nullptr;
    }

public: // 具体操作
    /*--- 入堆操作 ---*/
    void push(int value)
    {
        if (size_ == cap_)
        {
            int *p = new int[2*cap_];
            memcpy(p, que_, cap_ * sizeof(int)); // 数组复制❗❗❗
            delete[] que_;
            que_ = p;
            cap_ *= 2;
        }

        if (size_ == 0) que_[size_] = value; // 只有一个元素，不需要进行上浮调整
        else siftUp(size_, value);
        size_++;
    }

    /*--- 出堆操作 ---*/
    void pop()
    {
        if (size_ == 0) throw "Container is empty(pop)!";

        size_--;
        if (size_ > 0) siftDown(0, que_[size_]);// 还有元素，需要进行堆的下沉调整
    }

    /*--- 是否为空 ---*/
    bool isEmpty() const {return size_ == 0;}

    /*--- 获取堆顶元素 ---*/
    int top() const
    {
        if (size_ == 0) throw "Container is empty(top)!";
        return que_[0];
    }

    /*---获取堆大小 ---*/
    int size() const {return size_;}

private: // 上浮 & 下沉，时间复杂度均为 O(logn)，空间复杂度为 O(1)；❗❗❗
    /*--- 上浮调整 ---*/
    void siftUp(int i, int value)
    {
        while (i > 0) // 最多计算到根节点，即索引0处
        {
            int father = (i - 1) / 2;
            if (cmp_(value, que_[father])) // 若当前节点大于其父节点
            {
                que_[i] = que_[father]; // 父节点下沉
                i = father;             // 更新当前节点为父节点
            } else break;
        }
        que_[i] = value; // 把value放到i处
    }

    /*--- 下沉调整 ---*/
    void siftDown(int i, int value)
    {
        while (i < size_ / 2) // i下沉不能超过最后一个有孩子的节点
        {
            int child = 2 * i + 1; // i的左孩子
            if (child+1 < size_ && cmp_(que_[child+1], que_[child])) child += 1; // i的右孩子的值大于左孩子
            if (cmp_(que_[child], value))
            {
                que_[i] = que_[child];
                i = child;
            } else break;
        }
        que_[i] = value;
    }

private:
    int *que_; // 指向动态扩容的数组
    int size_; // 数组元素的个数
    int cap_;  // 数组的空间大小
    Cmp cmp_;  // 比较器
};

int main()
{
    PriorityQueue que;
    srand(time(NULL)); // 生成时间数
    for (int i = 0; i < 10; i++) que.push(rand() % 100); // 入堆
    while (!que.isEmpty()) // 出堆
    {
        cout << que.top() << " ";
        que.pop();
    }
    cout << endl;
    system("pause");
    return 0;
}
```

2. **C语言**代码：
```C
// 此处使用的是大根堆
#include <stdio.h>
#include <limits.h> // pop&top函数中要使用INT_MIN
#define MAX_SIZE 100

typedef struct
{
    int data[MAX_SIZE];
    int size;
} priorityQueue;

void init(priorityQueue *pq);               // 初始化优先队列，必须使用指针，不然就达不到修改地址所处位置的值
void swap(int *a, int *b);                  // 交换两个整数，必须使用指针！！！不然修改不了值
void heapifyUp(priorityQueue *pq, int i);   // 上浮操作（用于插入元素后维护堆性质）
void heapifyDown(priorityQueue *pq, int i); // 下沉操作（用于删除堆顶元素后维护堆性质）
void push(priorityQueue *pq, int value);    // 插入元素
int pop(priorityQueue *pq);                 // 删除并返回最大元素
int top(priorityQueue *pq);                 // 获取堆顶元素（不删除它）
int empty(priorityQueue *pq);               // 判断是否为空
int size(priorityQueue *pq);                // 获取大小
void print(priorityQueue *pq);              // 打印优先队列

void init(priorityQueue *pq)
{
    pq->size = 0;
}

void swap(int *a, int *b)
{
    int temp = *a;
    *a = *b;
    *b = temp;
}

void heapifyUp(priorityQueue *pq, int i) // 让位置i的值上浮
{
    while (i > 0) // 最多移到根节点——data[0]位置处
    {
        int parent = (i - 1) / 2;
        if (pq->data[i] <= pq->data[parent]) break; // 子节点值 <= 父节点值，不用上浮
        swap(&pq->data[i], &pq->data[parent]);
        i = parent;
    }
}

void heapifyDown(priorityQueue *pq, int i) // 让位置i的值下沉
{
    int largest = i;
    int l = 2 * i + 1, r = 2 * i + 2;

    // 找到父节点和两个子节点中的最大值
    if (l < pq->size && pq->data[l] > pq->data[largest]) largest = l;
    if (r < pq->size && pq->data[r] > pq->data[largest]) largest = r;

    // 如果最大值不是父节点，则交换并继续下沉
    if (largest != i)
    {
        swap(&pq->data[i], &pq->data[largest]);
        heapifyDown(pq, largest);
    }
}

void push(priorityQueue *pq, int value)
{
    if (pq->size >= MAX_SIZE) // 满了
    {
        printf("Priority queue is full!\n");
        return;
    }

    pq->data[pq->size] = value;
    heapifyUp(pq, pq->size); // 上浮
    pq->size++;
}

int pop(priorityQueue* pq)
{
    if (pq->size <= 0)
    {
        printf("Priority queue is empty!\n");
        return INT_MIN;
    }

    int maxValue = pq->data[0];
    pq->data[0] = pq->data[pq->size-1]; // 把最后一个节点设为根节点，再下沉
    pq->size--;
    heapifyDown(pq, 0); // 下沉

    return maxValue; // 返回最大元素
}

int top(priorityQueue *pq)
{
    if (pq->size <= 0)
    {
        printf("Priority queue is empty!\n");
        return INT_MIN;
    }
    return pq->data[0]; // 根节点即为max
}

int empty(priorityQueue *pq)
{
    return pq->size == 0;
}

int size(priorityQueue *pq)
{
    return pq->size;
}

void print(priorityQueue *pq)
{
    printf("Priority Queue: ");
    for (int i = 0; i < pq->size; i++)
        printf("%d ", pq->data[i]);
    printf("\n");
}

int main()
{
    priorityQueue pq;
    init(&pq);
    
    // 测试插入操作
    printf("插入元素: 10, 20, 15, 30, 40\n");
    push(&pq, 10);
    push(&pq, 20);
    push(&pq, 15);
    push(&pq, 30);
    push(&pq, 40);
    
    print(&pq);
    printf("堆顶元素: %d\n", top(&pq));
    printf("优先队列大小: %d\n", size(&pq));
    
    // 测试删除操作
    printf("\n删除堆顶元素:\n");
    while (!empty(&pq))
        printf("弹出: %d\n", pop(&pq));
    
    // 测试空队列
    printf("\n尝试从空队列弹出元素:\n");
    pop(&pq);
    
    return 0;
}
```