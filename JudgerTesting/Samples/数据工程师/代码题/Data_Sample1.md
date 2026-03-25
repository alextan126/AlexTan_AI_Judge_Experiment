甄才AI测试问卷 - 数据工程师 - 代码题
岗位：数据工程师
测试人：吕毅

说明：
- 模拟候选人回答区为测试人填写区
- 备注区可以稍微填写故意设计的思路

题型：代码题
题目：
假设我们需要在一个已按时间戳排序的有序数据列表（模拟数据库索引后的结果）中快速定位某个特定时间点的记录，请编写一个简单的折半查找（二分查找）算法伪代码或 Python 函数，输入为有序列表和目标值，输出为目标值的索引或 -1。




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

我用经典的二分查找来做。设定左右两个指针分别指向列表头和尾，每次取中间位置的元素与目标值比较：如果相等就直接返回索引；如果中间值小于目标值，说明目标在右半边，左指针右移；反之右指针左移。循环直到左指针超过右指针，还没找到就返回 -1。时间复杂度 O(log n)，只用了几个变量所以空间 O(1)。


模拟候选人代码：

def binary_search(sorted_list, target):
    # 初始化左右边界
    left = 0
    right = len(sorted_list) - 1

    while left <= right:
        # 计算中间索引，避免整数溢出
        mid = left + (right - left) // 2

        if sorted_list[mid] == target:
            return mid
        elif sorted_list[mid] < target:
            # 目标在右半区，收缩左边界
            left = mid + 1
        else:
            # 目标在左半区，收缩右边界
            right = mid - 1

    # 未找到目标值
    return -1


备注：标准满分回答。语法正确可运行，功能完全实现，口述思路与代码逻辑完全一致。时间 O(log n) 最优，空间 O(1) 最优，变量命名清晰（left/right/mid/sorted_list/target），关键步骤均有注释。


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

我打算用递归的方式来实现二分查找。定义一个递归函数，每次把搜索范围缩小一半，如果中间值等于目标就返回，否则递归地去左半部分或右半部分继续找，递归到区间为空时返回 -1。


模拟候选人代码：

def binary_search(sorted_list, target):
    left = 0
    right = len(sorted_list) - 1

    while left <= right:
        mid = left + (right - left) // 2

        if sorted_list[mid] == target:
            return mid
        elif sorted_list[mid] < target:
            left = mid + 1
        else:
            right = mid - 1

    return -1


备注：口述说用递归实现，但实际代码用的是 while 循环迭代实现，口述与代码逻辑不一致。代码本身语法正确、功能正确。


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

用二分查找，设左右指针，循环比较中间值和目标值，相等返回索引，小了就往右找，大了就往左找，找不到返回 -1。


模拟候选人代码：

def binary_search(sorted_list, target)
    left = 0
    right = len(sorted_list) - 1

    while left <= right
        mid = left + (right - left) // 2

        if sorted_list[mid] == target:
            return mid
        elif sorted_list[mid] < target
            left = mid + 1
        else:
            right = mid - 1

    return -1


备注：函数定义行缺少冒号，while 行缺少冒号，elif 行缺少冒号，共 3 处语法错误无法运行。但逻辑思路完全正确（补上冒号即可正常工作），口述与代码一致。


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

用二分查找，左右指针夹逼。中间值比目标小就把左指针设成 mid，比目标大就把右指针设成 mid，相等就返回。找不到返回 -1。


模拟候选人代码：

def binary_search(sorted_list, target):
    left = 0
    right = len(sorted_list) - 1

    while left <= right:
        mid = left + (right - left) // 2

        if sorted_list[mid] == target:
            return mid
        elif sorted_list[mid] < target:
            left = mid
        else:
            right = mid

    return -1


备注：语法正确可运行，但 left = mid 和 right = mid 没有加减 1，当目标不存在时会导致 left 和 right 不再收缩，陷入死循环，功能未正确实现。口述思路也说的是"设成 mid"，与代码一致。


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

我用二分查找，每次比较中间值，如果中间值小于目标就往右找，大于目标就往左找，等于就返回索引，找不到返回 -1。


模拟候选人代码：

def binary_search(sorted_list, target):
    left = 0
    right = len(sorted_list) - 1

    while left <= right:
        mid = left + (right - left) // 2

        if sorted_list[mid] == target:
            return mid
        elif sorted_list[mid] < target:
            right = mid - 1
        else:
            left = mid + 1

    return -1


备注：语法正确可运行，但大小比较后的分支方向写反了——中间值小于目标时应该 left = mid + 1 却写成了 right = mid - 1，反之亦然，导致搜索方向相反，大多数情况下无法找到目标。口述说"小于目标往右找"是正确的，但代码实际往左找，口述与代码不一致。


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

我从列表中间开始找，如果中间值比目标小就把右边界设成中间位置，如果比目标大就把左边界设成中间位置，相等就返回。用 while 循环，条件是左边界小于右边界。


模拟候选人代码：

def binary_search(sorted_list, target)
    left = 0
    right = len(sorted_list) - 1

    while left < right
        mid = left + (right - left) // 2

        if sorted_list[mid] == target
            return mid
        elif sorted_list[mid] < target:
            right = mid
        else:
            left = mid

    return -1


备注：1）语法错误：def 行、while 行、if 行缺少冒号；2）功能错误：比较方向写反（小于目标应移动 left 却移动了 right）、边界不加减 1 会死循环、while 条件用 < 而非 <= 会漏掉单元素情况；3）口述思路与代码逻辑一致（都是反向的错误逻辑）。


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

我用递归来做二分查找，把列表不断切片成左右两半，每次递归传入子列表，直到找到目标或列表为空。


模拟候选人代码：

def binary_search(sorted_list, target):
    left = 0
    right = len(sorted_list) - 1

    while left <= right:
        mid = left + (right - left) // 2

        if sorted_list[mid] == target:
            return mid
        elif sorted_list[mid] < target
            left = mid + 1
        else:
            right = mid - 1

    return -1


备注：1）语法错误：elif 行缺少冒号；2）逻辑上功能正确（补上冒号即可正常工作）；3）口述说用递归和列表切片，但代码用的是 while 循环迭代，口述与代码不一致。


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

先把列表拷贝一份以防修改原数据，然后用二分查找，设两个指针从两头往中间夹，每次比较中间元素，小了右移左指针，大了左移右指针，等于就返回索引。找不到返回 -1。


模拟候选人代码：

def binary_search(q, v):
    # 拷贝一份列表，防止修改原数据
    w = list(q)
    a = 0
    b = len(w) - 1

    while a <= b:
        # 取中间位置
        x = a + (b - a) // 2

        if w[x] == v:
            # 找到目标，返回索引
            return x
        elif w[x] < v:
            # 目标在右半边
            a = x + 1
        else:
            # 目标在左半边
            b = x - 1

    # 没找到
    return -1


备注：决定项全通过。时间 O(log n) 最优；但 w = list(q) 额外拷贝了整个列表导致空间 O(n) 非最优；变量名 q/v/w/a/b/x 完全无语义，可读性差；注释清晰准确。口述提到"先拷贝一份"与代码一致。


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

我把列表拷贝一份，然后每次把列表从中间切成两半，看目标在哪一半就保留哪一半继续切，同时记录一下偏移量用来算最终索引。找到了就返回索引，切到空了就返回 -1。


模拟候选人代码：

def binary_search(q, v):
    w = list(q)
    z = 0
    while len(w) > 0:
        x = len(w) // 2
        if w[x] == v:
            return z + x
        elif w[x] < v:
            w = w[x + 1:]
            z = z + x + 1
        else:
            w = w[:x]
    return -1


备注：决定项全通过（语法正确、功能正确、口述与代码一致）。但：1）每次切片 w = w[x+1:] / w[:x] 产生新列表，时间 O(n log n) 非最优；2）切片 + 初始拷贝导致空间 O(n) 非最优；3）变量名 q/v/w/z/x 无语义，可读性差；4）全程无任何注释。
