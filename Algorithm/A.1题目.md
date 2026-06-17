# 一、中心扩展法
## 1. [5. 最长回文子串 - 力扣（LeetCode）](https://leetcode.cn/problems/longest-palindromic-substring/description/)
这题可以使用**中心扩展法**+**动态规划**来解决。

---
# 二、LCA（最近公共祖先）
## 1. [236. 二叉树的最近公共祖先 - 力扣（LeetCode）](https://leetcode.cn/problems/lowest-common-ancestor-of-a-binary-tree/description/?envType=study-plan-v2&envId=top-100-liked)
## 2. [洛谷二叉树问题](https://www.luogu.com.cn/problem/P3884)
第（2）题使用了第（1）题的思路，第二题还包括**求二叉树的深度、宽度、两个节点的距离**以及**层次遍历**，难度在线。

---
# 三、并查集
## 1. [亲戚](https://www.luogu.com.cn/problem/P1551)
## 2. [村村通](https://www.luogu.com.cn/problem/P1536)
两题都是经典的**并查集**题型。
## 3. [集合](https://www.luogu.com.cn/problem/P1621)
这题只是普通的并查集，只是加了**素数**和[[#五、找q的大于等于a的最小倍数#1. [集合](https //www.luogu.com.cn/problem/P1621)|集合]]
## 4. [家谱](https://www.luogu.com.cn/problem/P2814)
这题涉及到了**字符串并查集**，之前做的都是数字，但是做法都差不多。
## 5. [团伙](https://www.luogu.com.cn/problem/P1892)
这题是**双数据并查集**，其中的敌人和朋友都是并的依据，并且使用了*unordered_set*
## 6. [程序自动分析](https://www.luogu.com.cn/problem/P1955)
这题使用了**并查集 + 离散化 + 哈希映射**的思路，真的很有挑战意义！其中的**离散化**是和**哈希映射**一起使用的：把数组先排序，再去重：`arr.erase(unique(all_node.begin(), all_node.end()), arr.end());`
*unique*的作用是***去除相邻的重复元素（这也是为什么要先排序），返回去重后有效区间的末尾迭代器***，然后使用*erase*去除掉重复部分。
再把数组中*离散的元素*通过*unordered_map*，*从0开始进行哈希映射*，从而实现离散化。这么做的原因是数据范围达到了`1e9`，这么多个*int*的内存达到了恐怖的*4GB*，但是*99%* 的内存是没用的。

---
# 四、哈希
## 1. [字符串哈希](https://www.luogu.com.cn/problem/P3370)
这是一道非常值得练习的题目，教会**字符串**怎么进行哈希。
## 2. [Cities and States](https://www.luogu.com.cn/problem/P3405)
这道题学到了不少东西，首先做法是使用**字符串哈希**，但是更重要的是*map*可以自增，我确实没想到！而且可以像数组那样初始化`map<int, int> m[100]`，可以`m[0][1] = 2，m[0][1]++`这些操作，但是后面问了豆包，***原来是map类型的数组，第一个[]是数组索引，第二个是map的键***。
## 3. [程序自动分析](https://www.luogu.com.cn/problem/P1955)
具体见[[#三、并查集#6. [程序自动分析](https //www.luogu.com.cn/problem/P1955)|程序自动分析]]

---
# 五、找q的大于等于a的最小倍数
## 1. [集合](https://www.luogu.com.cn/problem/P1621)
这道题是**并查集 + 素数 + ↑**，求的方式是`(a + q - 1) / q * q`。

---
# 六、离散化
## 1. [程序自动分析](https://www.luogu.com.cn/problem/P1955)
具体见[[#三、并查集#6. [程序自动分析](https //www.luogu.com.cn/problem/P1955)|程序自动分析]]

---
# 七、图的构造
## 1. [查找文献](https://www.luogu.com.cn/problem/P5318)
这题考察**图的邻接表**表示法，以及**DFS、BFS**，还有一点是我本来想用**指针+set**的方式来表示的，但是内存超了，所以改用**数组**方式。而且学到了***当set元素是自定义的类型时，怎么给set排序***，这个方法也适用于其他*自排序的STL类*：
```cpp
// 有先后顺序，不能更改结构体与运算符重载顺序
struct Node;
struct CompareNodePtr {
    bool operator()(const Node* a, const Node* b) const;
};
struct Node {
    int id;
    set<Node*, CompareNodePtr> references;
};
bool CompareNodePtr::operator()(const Node* a, const Node* b) const {
    return a->id < b->id;
}
```
## 2. [Cow Picnic S](https://www.luogu.com.cn/problem/P2853)
这题采用了**反向邻接表**来解题，此外还要*加强练习图的DFS*。

---
# 八、图的应用
## 1. [杂务](https://www.luogu.com.cn/problem/P1113)
这题使用的是**关键路径 + 拓扑排序 + 动态规划**，由于题目中说：*活动k的前置活动一定在[1~k-1]之间*。*所以相当于自动进行拓扑排序了*，所以只需要另外两个算法。而***动态规划是关键路径的必备，使用dp存储每个活动的最早结束时间***，所以只要处理**关键路径**就可以了，具体处理方式见提交的题目代码。
## 2. [最大食物链计数](https://www.luogu.com.cn/problem/P4017)
这题是**拓扑排序+dp**，还有**入度，出度**这两个顶点性质，知道使用什么方法后难度不大。
## 3. [最长路](https://www.luogu.com.cn/problem/P1807)
这题是**拓扑排序 + dp**，其实也可以认为是**关键路径**，因为*输入数据已经完成拓扑排序了*，所以*按照关键路径*方式做就可以了。
## 4. [排序](https://www.luogu.com.cn/problem/P1347)
这题是***判断有向无环图***。

---
# 九、偏移量
## 1. [幻象迷宫](https://www.luogu.com.cn/problem/P1363)
这题AI给的题解中出现了**偏移量**这个概念，它是指***一个坐标图中，当前位置与出发位置的(x, y)的相对位置***，比如说从(1, 2)出发，现在在(2, -3)，表示*在初始位置的下方一格，左方5格*，(1, -5)就是当前位置的偏移量。

---
# 十、求包含某子串且子串长度相同的子串的个数
## 1. [转录](https://www.luogu.com.cn/problem/T763396?contestId=326688)

---
# 十一、位运算
## 1. [找筷子](https://www.luogu.com.cn/problem/P1469)
这题是：一群数字中，只有一个数字的出现次数是奇数，其他数字的出现次数都是偶数，怎么找到这个出现次数为奇数的数字？使用**异或**运算即可，因为`a ^ a = 0, a ^ 0 = a`，*出现奇数次的数字异或结束后还是自己*。

---
# 十二、杨辉三角
## 1. [组合数问题](https://www.luogu.com.cn/problem/P2822)
这题是将*组合数*看成**杨辉三角**，构造出*组合数杨辉三角*。

---
# 十三、组合数
## 1. [组合数问题](https://www.luogu.com.cn/problem/P2822)
正如[[#十二、杨辉三角#1. [组合数问题](https //www.luogu.com.cn/problem/P2822)| 组合数问题]]所说的，将组合数构造成杨辉三角，而为什么可以构造成呢？因为组合数有一个重要性质：`C[m][n] = C[m-1][n] + C[m-1][n-1]`，比如：
`C[5][3] = 10 = C[4][3] + C[4][2] = 4 + 6`。而*杨辉三角就是：当前位置等于头顶两个数字相加*，即`T[i][j] = T[i-1][j] + T[i-1][j-1]`。
## 2. [直线交点数](https://www.luogu.com.cn/problem/P2789)
这题考察到一个知识点：***平面内的n条直线，若直线不重合 && 没有三点共线，最多可以有 C(n, 2)，即 n(n-1)/2 个交点***，这题正是利用了这个定理。
```txt
证明：
∵ 直线不重合
∴ 每两条直线最多产生1个交点
∵ 没有三点共线
∴ 要让交点数最多，必须让每一对直线都相交
∴ 第1条和其他n-1条直线组成一对，产生n-1个交点；第2条和除第1条外的其他n-2条直线组成一对，产生n-2个交点...第n-1条和除第1~n-2条外的直线组成一对，产生1个交点；第n条和除第1~n-1条直线外的直线组成一对，产生0个交点。
将它们相加，就是一个 an = N-n 的等差数列，求和：
Sn-1 = (n-1) + (n-2) + ... + 2 + 1 + 0 = n(n-1)/2

可以理解为从n条直线中选出2条相交的直线，那么就有 C(n, 2)种选择，而每两条相交的直线有1个交点，所以 max_points = C(n, 2) * 1 = C(n, 2)个。
```
## 3. [安全系统](https://www.luogu.com.cn/problem/P2638)
这题考的是高中很经典的题：*将m个完全相同的小球放入n个不同的箱子中，问有多少种方法*。这类题型有4种情况，都是用**挡板法**求解的：
（1）每个箱子至少放一个，小球必须放完；
（2）箱子可以为空，但是小球必须放完；
（3）每个箱子至少放一个，小球可以不放完；
（4）箱子可以为空，小球可以不放完。
```txt
对于（1）：因为每个箱子至少放一个，所以要用 n-1 个挡板来分隔这 m 个球，而 m 个球之间有 m-1 个位置可以放挡板，所以相当于是从 m-1 个位置选 n-1 个位置：ans = C[m-1][n-1]

对于（2）：箱子可以为空，那么我们就再加 n 个球，让每个箱子都先放一个，这样就变成问题（1）了：每个箱子至少一个，所以：ans = C[m+n-1][n-1]（m+n-1 个位置选 n-1 个位置）

对于（3）：先让每个箱子都有一个，那么还剩下 m-n 个，然后就是情况（4）了：m-n 个球放入 n 个箱子，箱子可以为空，小球可以不放完，所以：ans = C[m-n+n][n] = C[m][n]

对于（4）：既然小球可以不放完，那么就加一个“垃圾桶”，剩余的小球放到垃圾桶里面去，那么就变成情况（2）了，所以：ans = C[m+n-1+1][n-1] = C[m+n][n]（要选 n 个位置）
```
本题考查的是第（4）种情况，并且使用了`C[m][n] = C[m-1][n] + C[m-1][n-1]`以及**高精度**算法。

---
# 十四、高精度
## 1. [安全系统](https://www.luogu.com.cn/problem/P2638)
本题使用了**高精度乘法**。

---
# 十五、素数、因数
## 1. [Patting Heads S](https://www.luogu.com.cn/problem/P2926)
这题使用的是最普通的素数判断函数，即*从 2 开始看 n % 2 == 0 ?*。
## 2. [线性筛素数](https://www.luogu.com.cn/problem/P3383)
这道题是求*第 k 小的素数*，数据很大，所以*不能给一个 k 再算一个*，而是要构建**素数表**，构建的方式有比较好的两种：
```cpp
// 暴力法就不展示了
using LL = long long;
const int MAX_N = 1e8 + 5;
vector<bool> is_prime(MAX_N, true);
vector<int> primes;

/*----- 埃氏筛法 时间复杂度：O(nloglogn) -----*/
void build_1()
{
    is_prime[0] = is_prime[1] = false;
    for (int i = 2; i < MAX_N; i++)
        if (is_prime[i])
        {
            primes.emplace_back(i);
            // 将i的倍数全改为false
            for (LL j = 1LL*i*i; j < MAX_N; j += i) is_prime[j] = false; 
        }
}

/*----- 线性筛（欧拉筛）时间复杂度：O(n) -----*/
void build_2()
{
    is_prime[0] = is_prime[1] = false;
    for (int i = 2; i < MAX_N; i++)
    {
        if (is_prime[i]) primes.emplace_back(i);
        // 让每个合数只被它的最小因子p筛一次，做到无重复筛选，所以时间复杂度为 O(n)
        for (int p : primes)
        {
            if (1LL * i * p >= MAX_N) break; // 乘积超范围，停止枚举素数，防止越界
            is_prime[i*p] = false;
            if (i % p == 0) break;
        }
    }
}
```

`if (i % p == 0) break;`这一步的原因：primes中的元素大小是*升序*的，若i能被p整除，那么*p就是i的最小因子*，现在不用筛，后面循环会自动筛，直接结束，避免被重复筛。比如：`prime = [2,3,5,7...]`
i = 4，p = 2，标记 2 * 4 = 8为合数，4 % 2 = 0，结束，而不是再遍历 p = 3,5...因为若 p = 3，则 i * p = 12，标记12为合数，但是后面 i = 6的时候，  i * p = 12，又要标记一次，重复标记了。

## 3. [素数密度](https://www.luogu.com.cn/problem/P1835)
这题是求出[L, R]范围内的素数个数，因为数据最大可以到`INT_MAX`，所以使用的是**区间筛**，先使用**埃氏筛法 Or 欧拉筛**筛出$\sqrt{R}$范围内的所有素数，如果一个数在 `[l, r]` 里是合数，它的最小质因数肯定不超过它的平方根，而它本身又 ≤ r，所以最小质因数一定 ≤ $\sqrt{R}$，所以遍历$\sqrt{R}$内的小素数p，从*第一个 >= L 的 p 的倍数开始，将[L, R]范围内的所有 p 的倍数 设为 false*，最后再遍历一遍`is_prime`数`true`的个数即可得到[L, R]范围内的素数个数。
这里求***第一个 >= L 的 p 的倍数***的方式是：`(a + b - 1) / p * p`。
此处`max((long long)(p*p), ((long long)(l+p-1))/p * p);`，使用`p * p`是因为所有小于`p²`的`p`的倍数（比如`2p, 3p, ..., (p-1)p`）都已经被*更小的质数*标记过了。例如：`p=5`时`2*5=10`被 2 标记过，`3*5=15`被 3 标记过，`4*5=20`被 2 标记过，所以从 `5²=25` 开始标记就足够了，避免重复工作。
```cpp
int count_primes(int l, int r)
{
    if (r == 1) return 0;
    if (l == 1) l = 2;

    int sqrt_r = sqrt(r);
    vector<int> primes = build_prime_table(sqrt_r); // 筛出根号R范围内的素数
    
    vector<bool> is_prime(r-l+1, true);
    for (int p : primes)
    {
        long long start = max((long long)(p*p), ((long long)(l+p-1))/p * p);
        for (long long j = start; j <= r; j += p)
        {
            is_prime[j-l] = false;
        }
    }
}
```

## 4. [细胞分裂](https://www.luogu.com.cn/problem/P1069)
这一题的精髓就是[[#十六、GCD 与 LCM#定理1：]]。并且我学到了：
***怎么求出 $p_1,p_2,\dots,p_k$ 和 $e_1,e_2,\dots,e_k$
```cpp
// 计算n的质因数p的指数，修改n的值
int countFactor(int& n, int p)
{
    int cnt = 0;
    while (n % p == 0)
    {
        cnt++;
        n /= p;
    }
    return cnt;
}

map<int, int> factors;
int tmp = N;
for (int p = 2; p*p <= tmp; p++) // 逐个遍历，找因子
	if (tmp % p == 0) // 找到一个因子
    {
        int cnt = countFactor(tmp, p); // 求指数
        m1_factor[p] = cnt;
    }
if (tmp1 > 1) m1_factor[tmp1] = m2; // 处理最后一个素因子
```

## 5. [约数研究](https://www.luogu.com.cn/problem/P1403)
$$
\begin{array}{l}
欧拉筛核心:只用最小质因子去合成 p×i,保证每个合数只被筛 1 次\\
互质两数乘积的因数个数 = 各自因数个数相乘
\end{array}
$$
***最普通的求质因子的方法***：遍历 1~$\sqrt{n}$，i | n 就存入一对因子（若`i == n/i`只存入 i）
```cpp
// 时间复杂度 O(√n)
vector<int> getFactor(int n)
{
	vector<int> res;
	for (int i = 1; i <= sqrt(n); ++i)
		if (n % i == 0)
		{
			res.push_back(i);
			if (i != n/i) res.push_back(n/i);
		}
		sort(res.begin(), res.end()); // 从小到大排序 return res;
}
```
这题是对于[1~n]范围内的所有整数ai，求ai的因数个数ki，最后求$\sum\limits_{i=1}^n ki$
由于这题的 $n <= 1e6$，所以直接枚举因数 i，*所有 i 的倍数 j = i,2i... <= n都包含因数 i*，所以 `d[j]++`，d[i]为 i 的因数个数。
```cpp
// 时间复杂度 O(nlogn)
vector<int> cnt(n + 1, 0);
// 倍数筛：统计每个数因数个数
for (int i = 1; i <= n; ++i)
	for (int j = i; j <= n; j += i)
		d[j]++;
```
对于 $n >= 1e7$ 的情况，要使用**线性欧拉筛**，根据[[#十六、GCD 与 LCM#定理1：]]：若 $x=p_1^{k_1}p_2^{k_2}\dots p_m^{k_m}$。则 $d[x]=(k_1+1)(k_2+1)\dots(k_m+1)$

因为每个质因子 $p_i$ 的指数是 $k_i$，对于每个 $p_i$，指数可以取的范围是[0~ki]，一共有$k_i + 1$种选择，所以所有指数的所有组合是 $(k_1+1)(k_2+1)\dots(k_m+1)$。
```cpp
// 时间复杂度 O(n)
// spf: smallest prime factor，最小质因子
const int N = 1e7 + 5;
int spf[N], d[N], cnt[N]; // spf最小质因子，d因数个数，cnt当前质因子指数
vector<int> prime;
void init(int n)
{
    d[1] = 1;
    for (int i = 2; i <= n; i++)
    {
        if (!spf[i]) // i是素数，i = p^1 = i^1
        {
            spf[i] = i; // 最小质因子设为自己
	        d[i] = 2;   // 质数因数只有1和自己
            cnt[i] = 1; // 最小质因子指数是1
            prime.push_back(i);
        }
        // 遍历所有已经找到的 素数
        for (int p : prime)
        {
	        // 欧拉筛核心：只用最小质因子去合成 p*i，保证每个合数只被筛 1 次，O(n)
	        // p > spf[i]，p大于i的spf，跳出循环
	        // 1LL*p*i > n，跳出循环
            if (p > spf[i] || 1LL*p*i > n) break;
            spf[p*i] = p;   // p是p*i的spf
            if (i % p == 0) // p | i ==> p就是i的spf
            {
                cnt[p*i] = cnt[i] + 1; // p^(k+1)，p*i相对于p的指数加1
                d[p*i] = d[i] / cnt[p*i] * (cnt[p*i] + 1);
                break; // 欧拉筛关键：后面更大质数不用再筛i*p
            } else // p不能整除i，gcd(p,i) = 1
            {
                cnt[p*i] = 1;      // p是p*i最小质因子，指数=1
                d[p*i] = d[i] * 2; // d[p*i] = d[p] * d[i]，而d[p] = 2(p是素数)
            }
        }
    }
}
```
`if (i % p == 0)`部分推导：
设：
$i = p^{k}\cdot t,\quad \gcd(p,t)=1,\quad k = cnt[i], \quad num=p⋅i=pk+1⋅t$
则：
num 的最小质因子仍是 p, p 的新指数：$\boldsymbol{k+1}$ `cnt[p*i] = cnt[i] + 1;`

根据**约数个数定理**：
$$
\begin{align}
d[i] &= (k+1)\cdot d(t) \\
d(num)=d(p\cdot i) &= \big((k+1)+1\big)\cdot d(t) \end{align}
$$
从第一式变形：$\displaystyle d(t)=\frac{d[i]}{k+1}=\frac{d[i]}{cnt[p*i]}$，注意：$k+1=cnt[p*i]$
代入第二式：$d(p\cdot i)=\frac{d[i]}{cnt[p*i]}\times \big((k+1)+1\big)=\frac{d[i]}{cnt[p*i]}\times \big((cnt[p*i])+1\big)$

*末尾 break 作用*（欧拉筛精髓）
当 $p\mid i$ 时，后面更大的质数 $p'>p$：
$i\times p'$ 的最小质因子是 p 而不是 $p'$，这个合数*后续会被更小的 p 筛出来*，现在不用处理，直接跳出内层循环，保证每个合数只被筛 1 次。

## 6.[因子和](https://www.luogu.com.cn/problem/P1593)
这题还是使用[[#十六、GCD 与 LCM#定理1：]]的质因数分解，此外还加入了**快速幂、费马小定理、等比数列**的知识。
*这题的求解思路*：
1. 求出$a$的质因子$p_i$及每个质因子的指数$k_i\times b$
2. 遍历所有质因子，对**等比数列**求和：$sum_i = \sum\limits_{i=0}^{k_i\times b} p_i=\frac{p_i^{k_i\times b}-1}{p_i-1}$
3. $ans = \prod\limits_{i=1}^{n} sum_i$
第二步中，要求$p_i^{k_i\times b}$，使用**快速幂**。
因为题目中要**取模**，而***模运算中没有除法***！所以要除以$p_i-1$，则要使用**乘法逆元**，即*除以pi - 1*相当于乘以$p_i-1$的**逆元**：
$$
(p_i-1)\times x \equiv 1 \pmod{MOD}
$$
而$x$就是$p_i-1$的**逆元**，那么，怎么求$x$呢？
看**费马小定理**：$a^{p-1}\equiv 1 \pmod{p}$
则 $a\times a^{MOD-2}\equiv 1 \pmod{MOD}$

所以 $p_i-1$ 的**逆元**就是 $(p_i-1)^{MOD-2}$，这个可以用**快速幂**求出
但是上式成立的条件是：$gcd(p_i-1,MOD)=1$，即$p_i-1$和$MOD$互质
```cpp
else
{
    int x = (quick_pow(p%MOD, t+1) % MOD - 1) % MOD; // pi^(ki*b)-1
    int y = quick_pow((p-1) % MOD, MOD-2) % MOD;     // pi-1的逆元
    sum = x * y % MOD;
}
```
而当 $p_i-1\mod MOD=0$时，有 $p_i\mod MOD=1$
那么$sum_i=p^0+p^1+\dots +p^{k_i\times b}$ 对 $MOD$ 取模，结果就是 $1+k_i\times b$
`if((p-1) % MOD == 0) sum = 1 + k * b;`
而当 $p_i\mod MOD=0$ ，即 $p_i$ 是 $MOD$ 的倍数时，$sum_i=1$
`else if (p % MOD == 0) sum = 1;`

---
# 十六、GCD 与 LCM
---
首先我想介绍两个定理:
### 定理1：
***任何一个大于 1 的正整数，都可以唯一地分解成有限个质数的乘积。***
即对于任意正整数 N，有：$N = p_1^{e_1} \times p_2^{e_2} \times \dots \times p_k^{e_k}$
其中 $p_1 < p_2 < \dots < p_k$ 是质数，$e_1,e_2,\dots,e_k$ 是正整数。
比如：288 = $2^{5} \times 3^{2}$，即 $2 \times 2 \times 2 \times 3 \times 3$。

### 定理2：
$gcd(a, b) \times lcm(a, b) = a \times b$
*证明：*
设 $gcd(a, b) = k$，则：
$$
\begin{cases}
a = k_1 \times k\\
b = k_2 \times k\\
gcd(\frac{a}{k},\frac{b}{k}) = gcd(k_1, k_2) = 1
\end{cases}
$$
所以 $lcm(a, b) = lcm(k_1 \times k, k_2 \times k) = lcm(k_1, k_2) \times k$
因为 $gcd(k_1,k_2) = 1$
所以 $lcm(k_1,k_2) = k_1 \times k_2$
所以 $gcd(a,b) \times lcm(a,b) = k \times k_1 \times k_2 \times k = a \times b$
*证毕*

---
## 1. [Hankson 的趣味题](https://www.luogu.com.cn/problem/P1072)
这题就是考察*定理2*的内容，对于题目中的*a0, a1, b0, b1*，已知：
$$
\begin{cases}
gcd(x, a_0) = a_1\\
lcm(x, b_0) = b_1\\
x \mod a_1 = 0\\
b_1 \mod x = 0\\
a_1 < (a_0, x, b_0) < b_1
\end{cases}
$$
所以
$$
\begin{cases}
gcd(\frac{x}{a_1},\frac{a_0}{a_1}) = 1\\
lcm(x,b_0) = \frac{x \times b_0}{gcd(x,b_0)} = b_1 => gcd(x,b_0)=\frac{x \times b_0}{b_1}\\
x \mod a_1 = 0\\
b_1 \mod x = 0\\
a_1 < (a_0, x, b_0) < b_1
\end{cases}
$$
所以
$$
\begin{cases}
gcd(\frac{x}{a_1},\frac{a_0}{a_1}) = 1\\
gcd(\frac{b_1}{b_0},\frac{b_1}{x}) = 1\\
x \mod a_1 = 0\\
b_1 \mod x = 0\\
a_1 < (a_0, x, b_0) < b_1
\end{cases}
$$
所以我们让 x 从 1 开始，到 $\sqrt{b_1}$ 为止（到 $\sqrt{b_1}$ 是因为：***一个数字的因数是成对出现的，而分割线就是***$\sqrt{b_1}$）
每个 x 都判断上式是否成立，并且还要判断 $y = b_1 \div x$ 是否满足上式，x 或 y 满足时 `ans++`。

## 2. [晨跑](https://www.luogu.com.cn/problem/P4057)
这题考察的是
$$LCM(a, b, c) = LCM(LCM(a,b),LCM(a,c))$$
并且在*求LCM*的时候，应该*先除再乘*，不然先乘的话数字太大了，这点类似于求组合数$C[i][j]$的最基础的方法：
```cpp
// 计算C(n,k)，返回unsigned long long，够用了
unsigned long long comb(int n, int k)
{
	if (k < 0 || k > n) return 0;
	if (k == 0 || k == n) return 1;
	// 利用对称性：C(n,k)=C(n,n-k)，减少计算量
	k = min(k, n - k);
	unsigned long long res = 1;
	for (int i = 1; i <= k; ++i)
	{
		// 关键：先乘(n-k+i)，再除以i
		// 数学上保证这一步一定能整除
		res = res * (n - k + i) / i;
	}
	return res;
}
```

## 3. [又是毕业季Ⅱ](https://www.luogu.com.cn/problem/P1414)
这题是：*从 n 个数字中取出 k(1<=k<=n) 个数字，让这k个数字的 gcd 是最大的*。这个问题因为有 $C[n][k]$ 种取法，所以只要 n 大一点一定会超时，所以不能暴力枚举所有组合。那怎么解决嘞？

***如果一个数 d 是 k 个数字的 gcd，那么这 k 个数字必须全都是 d 的倍数。反过来，如果数组中有至少 k 个数字是 d 的倍数，那么我们一定可以选出这 k 个数字，它们的 gcd至少是 d。***

因此问题转化为：对于每个 k(1≤k≤n)，*找到最大的整数 d*，使得*数组中是 d 的倍数的数字个数大于等于k*。
$$
\begin{array}{l}
时间复杂度：O(n + mlogm)，m 为 maxElement。\\
空间复杂度：O(m)
\end{array}
$$
算法步骤：
（1）*统计频率*：统计数组中每个数字出现的次数
```cpp
// 统计每个分数的出现次数
vector<int> frequence(max_score+1, 0);
for (int i = 0; i < n; i++) frequence[score[i]]++;
```
（2）*倍数计数*：对于每个可能的 d，计算数组中有多少个数字是 d 的倍数
```cpp
// 统计g的倍数的出现次数cnt[g]
vector<int> cnt(max_score+1, 0);
for (int g = 1; g <= max_score; g++)
    for (int f = g; f <= max_score; f += g) // f = k * g (k = 1, 2, 3...)
        cnt[g] += frequence[f];
```
（3）*逆序填充答案*：从最大的 d 开始向下遍历，为每个 k 赋值最大的可能 gcd
```cpp
vector<int> ans(n+1, 0);
int cur = 0; // 表示已经判断了cur个人的情况
for (int g = max_score; g > 0 && cur < n; g--)
{
    if (cnt[g] <= cur) continue; // 要cur+1个人时，没那么多人的公共 gcd = g
    for (int k = cur+1; k <= cnt[g] && k <= n; k++) ans[k] = g; // k个人的情况
    cur = cnt[g]; // 更新已经判断了的人数
}
```

---
# 十七、快速幂
## 1. [因子和](https://www.luogu.com.cn/problem/P1593)
这题使用了**快速幂**，所谓**快速幂**就是快速地求出一个数字的高次幂的算法。
传统的求幂的方法是：
```cpp
int ans = 1;
for (int i = 1; i <= n; i++) ans *= ans;
```
这样的时间复杂度为：O(n)
而使用快速幂的时间复杂度为：O(logn)
```cpp
int quick_pow(int a, int b)
{
    int res = 1;
    while (b)
    {
        if (b & 1) res = res * a % MOD; // 数字大的话要 取模
        a = a * a % MOD;
        b >>= 1;
    }
    return res;
}
```

---
# 十八、费马大、小定理，欧拉函数、定理
---
### 费马大定理
对于所有的正整数 $a,b,c$ 和 $n$，当 $n>2$ 时
$$
a^n+b^n=c^n没有整数解
$$

### 费马小定理：
$$
对于任意整数a，素数p，有a^{p}\equiv p \pmod{p}
$$
$$
若gcd(a,p)=1，则a^{p-1}\equiv 1 \pmod{p}
$$

### 欧拉函数、定理
**欧拉函数** $\varphi(n)$ 表示 $\set{0,1,2,\dots,n-1}$ 内和 n 互素的元素个数。
若 $isPrime(n)$，则 $\varphi(n)=n-1$，否则，$\varphi(n)<n-1$。
**欧拉定理**：设 $a$ 与 $n$ 互素，则
$$
a^{\varphi(n)}\equiv 1 \pmod{n}
$$
这个其实就是**费马小定理**。具体可以看：*离散数学课本 P382*。

---
## 1. [因子和](https://www.luogu.com.cn/problem/P1593)
这题使用了**费马小定理**来求解**乘法的逆元**。

## 2.[签到题](https://www.luogu.com.cn/problem/P3601)
这题使用了**欧拉函数**，然后豆包还给出**杜教筛**:$O(n^\frac{2}{3})$ 的解决方法，但是题目的数据是：$10^{12}$，使用时达到了 $10^8$，而*C++ 最多是*：$10^8$，所以通过不了。***我现在做不来，等后面我完全理解了杜教筛和其他的方法后再做吧！***