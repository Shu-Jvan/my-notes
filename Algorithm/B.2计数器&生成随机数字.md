### 一、 使用头文件 `#include <chrono>`
这是C++中精度最高的计时方式
```cpp
#include <iostream>
#include <chrono>

int main()
{
    // 记录开始时间
    auto start = std::chrono::high_resolution_clock::now();
    
    // 这里是你要测量的代码
    for (int i = 0; i < 1000000; i++)
    {
        // 模拟工作负载
    }
    
    // 记录结束时间
    auto end = std::chrono::high_resolution_clock::now();
    
    // 计算并输出不同单位的时间
    auto duration_ns = std::chrono::duration_cast<std::chrono::nanoseconds>(end - start);  // 纳秒(ns)
    auto duration_ms = std::chrono::duration_cast<std::chrono::milliseconds>(end - start); // 毫秒(ms)
    auto duration_s  = std::chrono::duration_cast<std::chrono::seconds>(end - start);      // 秒(s)
    
    std::cout << "运行时间: " << duration_ns.count() << " 纳秒" << std::endl;
    std::cout << "运行时间: " << duration_ms.count() << " 毫秒" << std::endl;
    std::cout << "运行时间: " << duration_s.count() << " 秒" << std::endl;
    
    return 0;
}
```

在C++中生成指定范围内的随机数主要有两种方法：传统的 `rand()` 函数和 C++11 引入的现代 `<random>` 库。下面的表格能帮你快速了解它们的核心区别。

| 特性 | 传统方法 (`rand()` 和 `srand()`) | 现代方法 (C++11 `<random>` 库) |
| :--- | :--- | :--- |
| **随机数质量** | 较低，周期性短，分布可能不均匀 | **高**，使用梅森旋转等优质算法，周期极长 |
| **易用性与安全性** | 需手动计算范围，易出错（如忘记设置种子） | **更安全简单**，分布对象自动处理范围 |
| **灵活性** | 只能生成均匀分布，其他分布需复杂数学转换 | **支持多种分布**（均匀、正态、伯努利等） |
| **推荐使用场景** | 简单的脚本、对随机性要求不高的快速原型 | 正式项目、模拟实验、游戏开发、需要高质量随机数的场景 |

### 二、使用现代 `<random>` 库（推荐）

这是目前**最推荐**的方法，因为它生成的随机数质量高，使用起来也更直观安全。

**基本用法模板：**
```cpp
#include <iostream>
#include <random> // 核心头文件

int main()
{
    // 1. 创建随机数引擎并设置种子
    std::random_device rd;  // 随机设备，用于获取真随机种子
    std::mt19937 gen(rd()); // 使用梅森旋转算法引擎，用rd()的输出来初始化

    // 2. 定义随机数的分布范围
    int lower_bound = 1;
    int upper_bound = 100;
    std::uniform_int_distribution<> dist(lower_bound, upper_bound); // 均匀整数分布

    // 3. 生成随机数
    int random_number = dist(gen); // 每次调用dist(gen)都会产生一个范围内的随机数

    std::cout << "随机数: " << random_number << std::endl;
    return 0;
}
```

**生成不同类型和范围的随机数：**
- **浮点数范围**（如 5.0 到 10.0）：
  ```cpp
  std::uniform_real_distribution<double> dist(5.0, 10.0);
  double random_double = dist(gen);
  ```
- **其他分布**（如正态分布）：
  ```cpp
  // 生成均值为0，标准差为1的正态分布随机数
  std::normal_distribution<double> normal_dist(0.0, 1.0);
  double normal_number = normal_dist(gen);
  ```

### 三、使用传统的 `rand()` 方法

这是C语言继承而来的方法，简单但有一些缺点，如随机数质量不高、分布可能不均匀。

**基本步骤：**
1. 使用 `srand()` 设置随机数种子，通常用当前时间 `time(NULL)`。
2. 使用 `rand()` 生成随机数。
3. 通过模运算 `%` 将结果映射到目标范围。

**生成 [a, b] 范围内的随机整数公式：**
```cpp
#include <iostream>
#include <cstdlib> // 用于 rand() 和 srand()
#include <ctime>   // 用于 time()

int main()
{
    std::srand(std::time(nullptr)); // 用当前时间初始化随机种子

    int a = 1, b = 100;
    int random_num = std::rand() % (b - a + 1) + a; // 核心公式

    std::cout << "随机数: " << random_num << std::endl;
    return 0;
}
```

**不同范围需求的公式：**
- `[a, b)`（含a不含b）：`rand() % (b - a) + a`
- `(a, b]`（不含a含b）：`rand() % (b - a) + a + 1`
- `[0, 1)` 之间的浮点数：`rand() / static_cast<double>(RAND_MAX)`

### 💡 关键要点与建议

1.  **种子（Seed）的重要性**：无论是传统方法还是现代方法，都需要用种子初始化随机数生成器。使用随时间变化的种子（如 `time(nullptr)` 或 `random_device`）才能保证每次程序运行产生不同的随机序列。如果使用固定种子，每次运行程序得到的随机数序列会完全相同，适用于需要可重复结果的调试场景。

2.  **关于 `rand() % N` 的陷阱**：直接使用 `rand() % N` 来产生 `[0, N-1]` 的随机数时，如果 `RAND_MAX % N != 0`，那么产生的随机数概率并不是完全均匀的，较小的数值出现的概率会略微更高。对于要求严格的场景，这是一个需要考虑的细节。`<random>` 库中的分布对象（如 `uniform_int_distribution`）会自动处理这个问题，保证分布均匀。

3.  **何时选择何种方法**：
    *   **学习和简单练习**：可以从 `rand()` 入手，理解基本原理。
    *   **课程作业、个人项目或正式开发**：**强烈建议使用 `<random>` 库**，它的代码意图更清晰，能避免很多传统方法的坑。
    *   **高性能或高安全性需求**：必须使用 `<random>` 库，并可能需要选择更强大的随机数引擎（如 `mt19937_64`）或用于加密的安全随机数生成器。