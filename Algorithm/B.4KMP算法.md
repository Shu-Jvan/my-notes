### 一、什么是KMP算法？
<p style="text-indent: 2em; margin-top: 0.2em; margin-bottom: 0.5em;"><strong>KMP算法</strong>（Knuth-Morris-Pratt算法）是一种高效的字符串匹配算法，用于在一个文本串中查找模式串的出现位置。
</p>
<strong>核心思想：</strong>
<p style="text-indent: 2em; margin-top: 0.2em; margin-bottom: 0.5em;">
KMP算法通过预处理模式串，构建一个"部分匹配表"（也称为next数组或failure function），当匹配失败时，利用这个表跳过不必要的比较，避免回溯文本串的指针，从而提高匹配效率。
</p>

**时间复杂度：O(n+m)**，其中n是文本串长度，m是模式串长度
相比朴素匹配算法的O(n*m)，KMP在处理大量文本时效率更高
不需要回溯文本串指针，适合处理流式数据

**应用场景：**
- 文本编辑器的查找功能
- 生物信息学中的DNA序列匹配
- 网络入侵检测系统
- 数据压缩算法
- KMP算法的关键在于理解next数组的构建和使用，它体现了"以空间换时间"的算法设计思想。

### 二、怎么实现？
<p style="text-indent: 2em; margin-top: 0.2em; margin-bottom: 0.5em;">
包含2个部分——构建<strong>next数组</strong>、进行匹配。
其中next[index]的值就是看patt在index位置时，patt[0,index]这一部分的<strong>最长的相同前后缀</strong>，例如：ABABCABAB为4，因为前缀ABAB与后缀ABAB一样，且为最长的共同前后缀。
由于我不会画图，所以就直接上代码吧，C代码里面有注释，C++就不注释了😁😁
</p>

**C语言：**
```c
#include <stdio.h>
#include <string.h>
#include <stdlib.h>

/*-----构建next数组-----*/
int* buildNext(char *s)
{
    int len = strlen(s);
    int *next = malloc(sizeof(int) * len); // next数组大小为patt的长度
    next[0] = 0;// 由于index = 0时，只有一个字符，没有共同前后缀，所以next[0] = 0;
    int prefixLen = 0;  // 开始时共同前后缀长度为0
    for (int i = 1; i < len; i++)
        if (s[prefixLen] == s[i]) // 找到相同的字符了
        {
            prefixLen++;       // 继续匹配下一个，即s[prefixLen+1] 与 s[i+1]
            next[i] = prefixLen;  // 更新next[i]为当前已经匹配了的最长的前后缀长度
        } else if (prefixLen != 0)  // 没有匹配成功，且前一个字符还是匹配成功了的
        {
            prefixLen = next[prefixLen-1]; // 此处是一个很巧妙的设置
            /*
                当不匹配时，只是说明s[prefixLen] != s[i]，但并不代表此时的最长前后缀长度为0
                例如：ABACTTTABAB
                当 i = 9，即位于最后一个A时，此时可知prefixLen = 2，继续——i++，prefixLen++（由第一个if那得到）
                那么当 i = 10，prefixLen = 3时，s[i] != s[prefixLen]，进入此else-if部分
                虽然ABAC != ABAB，但是我们发现：它们有公共前后缀 AB，所以按理来说next[i]应为2
                但是我们不想重新遍历一次，怎么办呢？
                我们知道，前缀是我们已经遍历过且next[0,prefixLen-1]是已知的
                那么我们让 prefixLen = next[prefixLen-1]
                因为如果s[prefixLen-1] != 0，那么s[0]一定等于s[prefixLen-1]
                这时再让s[i]与s[prefixLen-1]进行判断，相等的话s[0]一定等于s[i-1]，这样就有了相同的前后缀
                例如此处的ABA，而s[i-1]为A，让j = s[prefixLen-1] = 1，再从已经匹配了的前缀（第一个A）开始和s[i]比对
            */                                                                                      //   ↑
            i--; // 因为for循环会加一次1，所以此处i--，以达到让i原地不动而与s[prefixLen（此时prefixLen已更新）]↑开始比对
        } else next[i] = 0; // 没有匹配成功且之前的i-1甚至i-2,……也没有匹配成功，说明一定不会有公共前后缀，next[i] = 0;
    return next;
}

/*-----进行匹配-----*/
int KMP(char *text, char *patt)
{
    int len1 = strlen(text), len2 = strlen(patt);
    if (len2 == 0) return 0;         // patt为空，一开始就匹配成功
    else if (len1 < len2) return -1; // 子串长度大于主串，不可能匹配
    int *next = buildNext(patt);
    int i = 0, j = 0;
    while (i < len1)
    {
        if (text[i] == patt[j]) i++, j++; // 匹配成功，继续
        else if (j == 0) i++;             // 匹配失败且之前也没有匹配成功，i++，继续匹配text[i]与patt[0]
        else j = next[j-1];               // 匹配失败且之前匹配成功了，那么让j从next[j-1]开始继续匹配，原因已在buildNext中说过

        if (j == len2) // 如果连续匹配成功的次数等于patt的长度，所以已经成功了，返回i-j，即patt第一个字符在text中成功匹配的索引
        {
            free(next);
            return i - j;
        }
    }
    free(next);
    return -1;
}

int main()
{
    char text[] = "Hello Avril!", patt[] = "Avril";
    printf("%d\n", KMP(text, patt));
    return 0;
}
```
<br>

**C++：**
```cpp
C++代码：
#include <iostream>
#include <vector>
#include <string>
using namespace std;

vector<int> buildNext(string s)
{
    vector<int> next;
    next.push_back(0);
    int i = 1, prefix_len = 0;
    while (i < (int)s.size())
    {
        if (s[prefix_len] == s[i])
        {
            prefix_len++, i++;
            next.push_back(prefix_len);
        } else if (prefix_len == 0)
        {
            next.push_back(0);
            i++;
        } else prefix_len = next[prefix_len - 1];
    }
    return next;
}

int KMP(string text, string patt)
{
    vector<int> next = buildNext(patt);
    int i = 0, j = 0, tLen = text.size(), pLen = patt.size();
    while (i < tLen)
    {
        if (text[i] == patt[j]) i++, j++;
        else if (j > 0) j = next[j-1];
        else i++;

        if (j == pLen) return i - j;
    }
    return -1;
}

int main()
{
    string text, patt;
    cin >> text >> patt;
    cout << KMP(text, patt) << endl;
    return 0;
}
```