### 一、欧几里得算法
**其实就是辗转相除法求最大公约数gcd**
***定理：*** gcd(a, b) = gcd(b, a%b)，其中a%b != 0，gcd(a, b)表示a与b的最大公约数
```cpp
// 1.
int get_gcd(int a, int b)
{
    if (b == 0) return a;
    else return get_gcd(b, a%b);
}
// 2.三目运算符
int get_gcd(int a, int b)
{
    return b == 0 ? a : get_gcd(b, a%b);
}
```

### 二、裴蜀定理
1. 若a，b是整数，且记 d = gcd(a,b)，那么对于任意的整数x，y，总有 ax + by是d的倍数
2. 对于给定的整数a，b，方程 ax + by = c有整数解的**充要**条件是c是gcd(a,b)的倍数

### 三、扩展欧几里得算法
**作用：** 
- **求模逆元：** 当 **gcd(a, m) = 1** 时，a 在模 m 下的逆元就是扩展欧几里得算法得出的 x，**(a * x) ≡ 1 (mod m)**
**逆元：** 对于非零整数a,m,如果存在b使得 **ab ≡ 1 (mod m)**，就称b是a在摸m意义下的逆元(inverse)
```cpp
int modInverse(int a, int m)
{
    int x, y;
    int gcd = extendedGCD(a, m, x, y);
    
    if (gcd != 1) return -1; // 模逆元不存在
    else
    {
        // 确保结果是正数
        int result = (x % m + m) % m;
        return result;
    }
}
```
- **解线性同余方程：** 求解 **ax ≡ b (mod m)**
- **解线性丢番图方程：** 求解 **ax + by = c**
- **中国剩余定理：** 在求解同余方程组时需要用到模逆元
- **密码学：** 在椭圆曲线密码学等现代密码系统中计算模逆元

**由裴蜀定理可知：** 对于给定的整数a，b，方程 **ax + by = gcd(a,b)** 总有整数解(x,y)，而现在我们要求出符合条件的整数解：
**gcd(a,b) = gcd(b,a%b)**
// 继续使用裴蜀定理
**b * x1 + (a%b) * y1 = gcd(b,a%b)** 有整数解x1，y1
**ax + by = b * x1 + (a%b) * y1**
**a%b = a - b * $\left\lfloor \frac{a}{b} \right\rfloor$**
**ax + by = b * x1 + (a - b * $\left\lfloor \frac{a}{b} \right\rfloor$) * y1**
**a * (x - y1) - b * (x1 - y - $\left\lfloor \frac{a}{b} \right\rfloor$ * y1) = 0**
// 让括号内的表达式 = 0（我也不知道为什么），则：
**x = y1，y = x1 - $\left\lfloor \frac{a}{b} \right\rfloor$ * y1**
// 递归终点：与欧几里得算法的递归中的类似，如果 b == 0，那直接取x = 1，y = 0便是满足等式的解

```cpp
// 要gcd就返回int———gcd，要解就用 void，因为是引用
int exgcd(int a, int b, int &x, int &y)
{
    if (b == 0)
    {
        x = 1, y = 0;
        return a;
    }
    int gcd = exgcd(b, a%b, y, x);
    y -= (a / b) * x;
    return gcd;
}
```

**习题：** https://www.luogu.com.cn/problem/P1082