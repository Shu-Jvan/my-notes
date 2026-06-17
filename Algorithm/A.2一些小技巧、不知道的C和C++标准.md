# 一、快读、快写
## (1)、为什么需要快读快写？
*核心原因*：默认的`cin/cout`速度极慢，在算法竞赛大数据量场景下（如*n ≥ 1e5，m ≥ 1e6*）会直接导致超时。

以常见的输入规模为例：
- 输入*1e6* 个整数：`cin` 未优化时需要约*1.2 秒*
- 同样数据：`scanf` 需要约 *0.3 秒*
- 手写快读：仅需约 *0.05 秒*
差距可达*20倍以上*，这是算法竞赛中必须掌握的基础优化。

---
## (2)、`cin/cout` 慢的根本原因
### 1. 与 C 标准 IO 的同步机制（最主要原因）
C++ 标准为了保证 `cin/cout` 和 `scanf/printf` 可以混合使用且输出顺序一致，*默认开启了stdio 同步*：
- 每次 `cin` 操作都会先刷新 `stdin` 缓冲区
- 每次 `cout` 操作都会先刷新 `stdout` 缓冲区
- 频繁的缓冲区刷新会产生大量系统调用，而系统调用是极其耗时的操作
### 2. `cout` 与 `cin` 的绑定机制
默认情况下，`cin` 和 `cout` 是绑定的：
- 每次执行 `cin >> x` 之前，都会*自动执行 `cout.flush()`
- 目的是保证提示信息（如 `cout << "请输入："`）在输入前显示
- 但在算法竞赛中，我们不需要这种交互，完全可以解绑
### 3. `endl` 的额外开销
`endl` 等价于 `'\n' + flush()`，*每次使用都会强制刷新缓冲区*。
- 输出 `1e6` 个 `endl` 会产生 `1e6` 次系统调用
- 而输出 `1e6` 个 `'\n'` *只会在缓冲区满时自动刷新*，通常只有几次系统调用

---
## (3)、最快的通用优化方案（99% 场景足够）
这是算法竞赛中最常用的优化，*一行代码解决 99% 的超时问题*，不需要修改任何输入输出代码：
```cpp
int main()
{
    // 关闭stdio同步 + 解绑cin和cout
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    // 之后正常使用cin/cout即可，速度接近scanf/printf
    int n;
    cin >> n;
    cout << n << '\n'; // 注意：用'\n'代替endl！

    return 0;
}
```
### 注意事项
1. *绝对不能混用*`cin/cout` 和 `scanf/printf`：关闭同步后，两者的缓冲区独立，输出顺序会混乱
2. *必须用*`'\n'`代替 `endl`：否则仍然会频繁刷新缓冲区
3. `cout.tie(nullptr)` *不是必须的*：因为我们只需要解绑`cin`对`cout`的依赖

---
## (4)、终极优化：手写快读快写（适用于`m ≥ 1e6`）
当数据量达到*百万级*以上时，即使优化后的 `cin/cout` 也可能不够快，这时需要手写基于 `getchar()`/`putchar()` 的快读快写。
### 原理
- `getchar()` 和 `putchar()` 是 C 标准库中***最快***的字符级输入输出函数
- 它们*直接操作标准 IO 缓冲区，没有任何额外开销*
- 我们自己实现整数/字符串的解析，避免标准库的通用处理开销
### 完整实现
```cpp
// 快读：读取一个整数（支持正负）
inline int read()
{
    int x = 0, f = 1;
    char ch = getchar();
    // 跳过所有非数字字符
    while (ch < '0' || ch > '9')
    {
        if (ch == '-') f = -1;
        ch = getchar();
    }
    // 解析数字
    while (ch >= '0' && ch <= '9')
    {
        x = x * 10 + (ch - '0');
        ch = getchar();
    }
    return x * f;
}

// 快写：输出一个整数（支持正负）
inline void write(int x)
{
    if (x < 0)
    {
        putchar('-');
        x = -x;
    }
    // 递归输出每一位（避免栈溢出，x最大为2e9时递归深度仅10）
    if (x > 9) write(x / 10);
    putchar(x % 10 + '0');
}

// 快写：输出一个字符
inline void write(char ch)
{
    putchar(ch);
}
```
### 使用示例

```cpp
int main()
{
    int n = read();
    for (int i = 0; i < n; i++)
    {
        int x = read();
        write(x);
        write('\n');
    }
    return 0;
}
```

---
## (5)、究极优化：基于`fread()`的超级快读（适用于`m ≥ 1e7`）
当数据量达到*千万级*时，即使 `getchar()` 也会因为频繁的函数调用变慢，这时需要使用 `fread()` *一次性读取整块数据到内存缓冲区*，然后自己解析。
### 原理
- `fread()` 可以一次性读取最多 `BUFSIZ` 字节的数据（通常是 8192 字节）
- 只需要一次系统调用，就能读取数千个字符
- 我们直接在内存缓冲区中解析数据，没有任何函数调用开销
### 实现代码
```cpp
const int BUF_SIZE = 1 << 20; // 1MB缓冲区
char buf[BUF_SIZE];
int buf_ptr = 0, buf_len = 0;

inline char get_char()
{
    if (buf_ptr == buf_len)
    {
        buf_len = fread(buf, 1, BUF_SIZE, stdin);
        buf_ptr = 0;
        if (buf_len == 0) return EOF;
    }
    return buf[buf_ptr++];
}

inline int read()
{
    int x = 0, f = 1;
    char ch = get_char();
    while (ch < '0' || ch > '9')
    {
        if (ch == '-') f = -1;
        ch = get_char();
    }
    while (ch >= '0' && ch <= '9')
    {
        x = x * 10 + (ch - '0');
        ch = get_char();
    }
    return x * f;
}
```

---
## (6)、性能对比表

| 方法            | 读取 1e6 个整数耗时 | 适用场景        |
| ------------- | ------------ | ----------- |
| 未优化的 cin      | ~1200ms      | 仅适用于小数据量测试  |
| 优化后的 cin      | ~200ms       | 99% 的算法竞赛题目 |
| scanf         | ~300ms       | 兼容 C 代码时使用  |
| 手写 getchar 快读 | ~50ms        | 百万级数据量      |
| fread 超级快读    | ~10ms        | 千万级数据量      |

---
# 二、不知道有多少（个 or 组）输入
| 场景           | 推荐写法                                                       |
| ------------ | ---------------------------------------------------------- |
| 有数值结束标志      | `while (cin >> num) { if (num == -1) break; }`             |
| 有字符结束标志（含空白） | `while (cin.get(ch)) { if (ch == 'q') break; }`            |
| 有字符串结束标志     | `while (getline(cin, line)) { if (line == "end") break; }` |
| 读取单个数据到 EOF  | `while (cin >> a) { ... }`                                 |
| 读取多个数据到 EOF  | `while (cin >> a >> b) { ... }`                            |
| 读取整行到 EOF    | `while (getline(cin, line)) { ... }`                       |
| 解析一行中的多个数据   | `getline + istringstream`                                  |
1. [幻象迷宫](https://www.luogu.com.cn/problem/P1363)
这题是没用结束标志的

---
# 三、求得一个数字的每一位
1. [高低位交换](https://www.luogu.com.cn/problem/P1100)
这道题是*提取一个整数的每一位*。
```cpp
void print_binary_32(int num)
{
    // 从最高位(31)到最低位(0)依次输出
    for (int i = 31; i >= 0; i--)
    {
        // 提取第i位
        int bit = (num >> i) & 1;
        printf("%d", bit);
        // 每4位加一个空格，方便阅读
        if (i % 4 == 0 && i != 0) printf(" ");
    }
    printf("\n");
}
```

---
# 四、类型混用
1. [车的攻击](https://www.luogu.com.cn/problem/P3913)
这题中我混用了**long long**和**int**，导致结果为**int**类型，并不是**long long**类型。

# 五、遍历 pair 技巧
之前我每次遍历一个`map`或者其他存储了`pair`类型的容器时，都是`auto it`，但是还有一种方式：`auto [p, k] : map`，这样*可以就直接使用 键 和 值 了*。注意`[p, k]`是值拷贝，*不会改变原键值对*。