甄才AI测试问卷 - 算法工程师 - 代码题
岗位：算法工程师
测试人：徐博研

说明：
- 模拟候选人回答区为测试人填写区
- 备注区可以稍微填写故意设计的思路

题型：代码题
题目：
假设在大规模文本数据预处理阶段，我们需要高效地检测用户输入中是否包含特定的敏感词串（模式串 T），已知主串 S 的长度为 N，模式串 T 的长度为 M。请写出基于 KMP 算法核心思想的 Python 代码片段（只需实现 next 数组构建及匹配循环的核心逻辑），并简要分析其时间复杂度为何优于朴素匹配算法。

————————

样本测试序号 K-01
填写时请满足以下要求：
    1. 代码语法正确，可以运行
    2. 功能完全实现，输出与预期一致
    3. 口述思路与代码逻辑一致
    4. 时间复杂度最优
    5. 空间复杂度最优
    6. 变量命名清晰，结构分明
    7. 关键步骤有注释


决定项：
        syntax_correct（语法是否正确）： 1（0/1）
        function_correct（功能是否实现）： 1（0/1）
        asr_match（ASR逻辑的对应性）： 1（0/1）

加分项：
        time_optimal（是否Tn最佳）： 1（0/1）
        space_optimal（是否Sn最佳）： 1（0/1）
        code_readability（代码可读性）： 1（0/1）
        comment_readability（注释可读性）： 1（0/1）


模拟候选人口述思路：
我会用 KMP 来做敏感词检测，先给模式串 T 构建 next 数组，表示当前位置之前最长相等前后缀的长度。匹配时用两个指针扫描主串和模式串，如果失配，就根据 next 数组回退模式串指针，而主串指针不回退。这样整体时间复杂度是 O(N+M)，比朴素匹配最坏情况下的 O(N*M) 更优。



模拟候选人代码：
def build_next(pattern):
    # next[i] 表示 pattern[:i+1] 中最长相等前后缀的长度
    nxt = [0] * len(pattern)
    j = 0

    for i in range(1, len(pattern)):
        # 失配时，根据 next 数组回退 j
        while j > 0 and pattern[i] != pattern[j]:
            j = nxt[j - 1]

        if pattern[i] == pattern[j]:
            j += 1

        nxt[i] = j

    return nxt


def kmp_contains(text, pattern):
    if pattern == "":
        return True

    nxt = build_next(pattern)
    j = 0

    for ch in text:
        # 当前字符失配，则让模式串指针回退
        while j > 0 and ch != pattern[j]:
            j = nxt[j - 1]

        if ch == pattern[j]:
            j += 1

        # 找到完整模式串
        if j == len(pattern):
            return True

    return False



备注：
标准 KMP 写法，语法正确，逻辑清晰，口述与代码一致，时间复杂度和空间复杂度都合理。


————————

样本测试序号 K-02
填写时请满足以下要求：
    1. 代码语法正确，功能实现
    2. 但口述思路与代码逻辑不一致（如口述说用递归，代码用循环）


决定项（任一=0 则加分项留空）：
        syntax_correct（语法是否正确）： 1（0/1）
        function_correct（功能是否实现）： 1（0/1）
        asr_match（ASR逻辑的对应性）： 0（0/1）

加分项（决定项存在=0，留空）：


模拟候选人口述思路：
我打算用递归方式来做，每次从主串的一个位置开始尝试匹配，如果失败就递归到下一个起点继续找。这样写起来会比较直观，也比较符合字符串搜索的思路。


模拟候选人代码：
def build_next(pattern):
    nxt = [0] * len(pattern)
    j = 0

    for i in range(1, len(pattern)):
        while j > 0 and pattern[i] != pattern[j]:
            j = nxt[j - 1]
        if pattern[i] == pattern[j]:
            j += 1
        nxt[i] = j

    return nxt


def kmp_contains(text, pattern):
    if pattern == "":
        return True

    nxt = build_next(pattern)
    j = 0

    for i in range(len(text)):
        while j > 0 and text[i] != pattern[j]:
            j = nxt[j - 1]
        if text[i] == pattern[j]:
            j += 1
        if j == len(pattern):
            return True

    return False


备注：
代码实际使用的是 KMP 的迭代双指针写法，而不是口述中的“递归枚举起点”，因此 asr_match=0。


————————

样本测试序号 K-03
填写时请满足以下要求：
    1. 代码有语法错误（如缺少冒号、括号不匹配等），无法运行
    2. 但从逻辑上看功能思路是对的
    3. 口述思路与代码逻辑一致


决定项：
        syntax_correct（语法是否正确）： 0（0/1）
        function_correct（功能是否实现）： 1（0/1）
        asr_match（ASR逻辑的对应性）： 1（0/1）

加分项（决定项存在=0，留空）：/


模拟候选人口述思路：
我会先构建模式串的 next 数组，记录每个位置可复用的最长公共前后缀长度。然后扫描主串，匹配失败时只回退模式串指针，不回退主串指针，这样能够在线性时间内完成匹配。


模拟候选人代码：
def build_next(pattern):
    nxt = [0] * len(pattern)
    j = 0

    for i in range(1, len(pattern)):
        while j > 0 and pattern[i] != pattern[j]:
            j = nxt[j - 1]
        if pattern[i] == pattern[j]:
            j += 1
        nxt[i] = j

    return nxt


def kmp_contains(text, pattern):
    if pattern == "":
        return True

    nxt = build_next(pattern)
    j = 0

    for ch in text:
        while j > 0 and ch != pattern[j]:
            j = nxt[j - 1]
        if ch == pattern[j]:
            j += 1
        if j == len(pattern)
            return True

    return False



备注：
逻辑上是正确的 KMP 实现，且与口述一致，但 if j == len(pattern) 后缺少冒号，存在明显语法错误，无法运行。


————————

样本测试序号 K-04
填写时请满足以下要求：
    1. 代码语法正确，可以运行
    2. 但功能没有实现（输出与预期不一致）
    3. 口述思路与代码逻辑一致


决定项：
        syntax_correct（语法是否正确）： 1（0/1）
        function_correct（功能是否实现）： 0（0/1）
        asr_match（ASR逻辑的对应性）： 1（0/1）

加分项（决定项存在=0，留空）：/


模拟候选人口述思路：
我是按 KMP 的思路写，先构建 next 数组。匹配的时候如果前面已经匹配了一部分但当前字符失配，我会让主串指针和模式串指针都往后调整，这样继续找下一个位置。


模拟候选人代码：
def build_next(pattern):
    nxt = [0] * len(pattern)
    j = 0

    for i in range(1, len(pattern)):
        while j > 0 and pattern[i] != pattern[j]:
            j = nxt[j - 1]
        if pattern[i] == pattern[j]:
            j += 1
        nxt[i] = j

    return nxt


def kmp_contains(text, pattern):
    if pattern == "":
        return True

    nxt = build_next(pattern)
    i, j = 0, 0

    while i < len(text) and j < len(pattern):
        if text[i] == pattern[j]:
            i += 1
            j += 1
        elif j > 0:
            i += 1          # 错误：这里不应该同时移动 i
            j = nxt[j - 1]
        else:
            i += 1

    return j == len(pattern)

备注：
语法正确，但失配时错误地同时移动了主串指针 i，会漏掉本应继续比较的字符，导致某些用例下匹配失败。口述和代码中的错误逻辑是一致的。


————————

样本测试序号 K-05
填写时请满足以下要求：
    1. 代码语法正确
    2. 功能没有实现
    3. 口述思路与代码逻辑也不一致


决定项：
        syntax_correct（语法是否正确）： 1（0/1）
        function_correct（功能是否实现）： 0（0/1）
        asr_match（ASR逻辑的对应性）： 0（0/1）

加分项（决定项存在=0，留空）：/


模拟候选人口述思路：
我会先构建标准的 next 数组，然后在匹配时如果失配，就按 next 数组回退模式串指针，主串继续向前扫描。这样就能避免重复比较，提高整体效率。


模拟候选人代码：
def build_next(pattern):
    return [0] * len(pattern)


def kmp_contains(text, pattern):
    if pattern == "":
        return True
    if len(text) < len(pattern):
        return False

备注：
代码语法正确，但功能没有完整实现，只比较了主串前缀，无法完成真正的子串搜索；同时口述说的是标准 KMP，和代码逻辑也不一致。


————————

样本测试序号 K-06
填写时请满足以下要求：
    1. 代码有语法错误
    2. 功能也没有实现
    3. 但口述思路与代码逻辑一致


决定项：
        syntax_correct（语法是否正确）： 0（0/1）
        function_correct（功能是否实现）： 0（0/1）
        asr_match（ASR逻辑的对应性）： 1（0/1）

加分项（决定项存在=0，留空）：/


模拟候选人口述思路：
我这里打算简化一下逻辑：如果匹配成功，就让两个指针一起前进；如果失配了并且模式串已经匹配了一部分，我也让两个指针一起往后走。整体还是双指针扫描的方式。


模拟候选人代码：
def kmp_contains(text, pattern):
    if pattern == "":
        return True

    i, j = 0, 0

    while i < len(text) and j < len(pattern):
        if text[i] == pattern[j]:
            i += 1
            j += 1
        elif j > 0
            i += 1
            j += 1
        else:
            i += 1

    return j == len(pattern)

备注：
一方面 elif j > 0 后缺少冒号，存在语法错误；另一方面失配时让 i 和 j 同时前进，逻辑本身也是错误的。口述和代码错误点一致。


————————

样本测试序号 K-07
填写时请满足以下要求：
    1. 代码有语法错误
    2. 从逻辑上看功能思路是对的
    3. 口述思路与代码逻辑不一致


决定项：
        syntax_correct（语法是否正确）： 0（0/1）
        function_correct（功能是否实现）： 1（0/1）
        asr_match（ASR逻辑的对应性）： 0（0/1）

加分项（决定项存在=0，留空）：/


模拟候选人口述思路：
我会直接用双重循环来做，外层枚举主串的每个起点，内层逐个字符比较模式串，只要全部相等就说明找到了。这个方法比较直接，也容易理解。

模拟候选人代码：
def build_next(pattern):
    nxt = [0] * len(pattern)
    j = 0

    for i in range(1, len(pattern))
        while j > 0 and pattern[i] != pattern[j]:
            j = nxt[j - 1]
        if pattern[i] == pattern[j]:
            j += 1
        nxt[i] = j

    return nxt


def kmp_contains(text, pattern):
    if pattern == "":
        return True

    nxt = build_next(pattern)
    j = 0

    for ch in text:
        while j > 0 and ch != pattern[j]:
            j = nxt[j - 1]
        if ch == pattern[j]:
            j += 1
        if j == len(pattern):
            return True

    return False



备注：
代码从逻辑上看是标准 KMP，功能思路是对的，但 for i in range(1, len(pattern)) 后缺少冒号，属于语法错误；同时口述说的是暴力双循环，和代码不一致。


————————

样本测试序号 K-08
填写时请满足以下要求：
    1. 代码语法正确，功能实现，口述一致（决定项全通过）
    2. 时间复杂度最优
    3. 但空间复杂度非最优（如用了额外数组拷贝）
    4. 变量名混乱（如用 a, b, x 命名）
    5. 有注释


决定项：
        syntax_correct（语法是否正确）： 1（0/1）
        function_correct（功能是否实现）： 1（0/1）
        asr_match（ASR逻辑的对应性）： 1（0/1）

加分项：
        time_optimal（是否Tn最佳）： 1（0/1）
        space_optimal（是否Sn最佳）： 0（0/1）
        code_readability（代码可读性）： 0（0/1）
        comment_readability（注释可读性）： 1（0/1）


模拟候选人口述思路：

我按 KMP 来写，先构建模式串的 next 数组，再用双指针做匹配。失配时主串指针不回退，只根据 next 去跳模式串的位置，所以时间复杂度仍然是线性的。只是我这里为了写起来方便，做了一些额外的数组拷贝。

模拟候选人代码：
def f(b):
    c = list(b)
    d = c[:]   # 额外拷贝，空间不是最优
    x = [0] * len(d)
    y = 0

    # x[i] 表示模式串到 i 为止的最长可复用前后缀长度
    for z in range(1, len(d)):
        while y > 0 and d[z] != d[y]:
            y = x[y - 1]
        if d[z] == d[y]:
            y += 1
        x[z] = y
    return x


def g(a, b):
    if b == "":
        return True

    s1 = list(a)
    s2 = list(b)
    s3 = s2[:]   # 额外拷贝，空间不是最优
    n = f(s3)

    i = 0
    j = 0

    # 主串一直向前走，失配时只调整模式串位置
    while i < len(s1):
        while j > 0 and s1[i] != s2[j]:
            j = n[j - 1]
        if s1[i] == s2[j]:
            j += 1
        if j == len(s2):
            return True
        i += 1

    return False



备注：
功能正确、时间复杂度仍是 O(N+M)，但做了不必要的列表和切片拷贝，空间不是最优；变量名如 a、b、c、d、x、y、z 较混乱，可读性差。不过注释是清楚的。


————————

样本测试序号 K-09
填写时请满足以下要求：
    1. 代码语法正确，功能实现，口述一致（决定项全通过）
    2. 但所有加分项都不通过：
       - 时间复杂度非最优
       - 空间复杂度非最优
       - 变量名混乱
       - 无注释


决定项：
        syntax_correct（语法是否正确）： 1（0/1）
        function_correct（功能是否实现）： 1（0/1）
        asr_match（ASR逻辑的对应性）： 1（0/1）

加分项：
        time_optimal（是否Tn最佳）： 0（0/1）
        space_optimal（是否Sn最佳）： 0（0/1）
        code_readability（代码可读性）： 0（0/1）
        comment_readability（注释可读性）： 0（0/1）


模拟候选人口述思路：
我这里做的是字符串匹配，不过写法上比较直接。我会从主串每个位置开始都重新尝试一遍，并且每次都重新处理模式串，这样虽然麻烦一点，但结果也能做出来。

模拟候选人代码：
def a(t):
    r = [0] * len(t)
    for i in range(1, len(t)):
        for j in range(i, 0, -1):
            if t[:j] == t[i - j + 1:i + 1]:
                r[i] = j
                break
    return r


def b(s, t):
    if t == "":
        return True
    for i in range(len(s)):
        x = s[i:]
        y = t[:]
        z = a(y)
        p = 0
        q = 0
        while p < len(x) and q < len(y):
            if x[p] == y[q]:
                p += 1
                q += 1
                if q == len(y):
                    return True
            else:
                break
    return False



备注：
代码可以运行，也能得到正确结果，口述与代码一致；但时间复杂度明显不是最优，存在大量重复计算和切片拷贝，空间复杂度也不佳；变量名混乱，且没有注释。