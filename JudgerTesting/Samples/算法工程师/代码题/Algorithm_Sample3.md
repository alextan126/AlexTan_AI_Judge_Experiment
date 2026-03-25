甄才AI测试问卷 - 算法工程师 - 代码题
岗位：算法工程师
测试人：徐博研

说明：
- 模拟候选人回答区为测试人填写区
- 备注区可以稍微填写故意设计的思路

题型：代码题
题目：
假设你需要实现一个基于滑动窗口的实时特征提取功能，利用队列数据结构处理流式数据。请编写一段简单的 Python 伪代码，实现将新数据入队并移除过期数据的逻辑，同时说明该操作的时间复杂度。

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
我会用一个队列来保存窗口内仍然有效的数据，每来一条新数据，就先把它入队。然后不断检查队首元素是否已经过期，如果过期就从队首移除，直到队首重新落回窗口范围内。这样每个元素最多入队和出队一次，所以单次更新的均摊时间复杂度是 O(1)，空间复杂度是 O(k)，其中 k 是窗口内元素个数。
模拟候选人代码：
from collections import deque

def update_window(window_queue, new_time, new_value, window_size):
    # 新数据入队，保存为 (时间戳, 数值)
    window_queue.append((new_time, new_value))

    # 移除所有过期数据：当前时间 - 数据时间 > 窗口大小
    while window_queue and new_time - window_queue[0][0] > window_size:
        window_queue.popleft()

    return window_queue

备注：
标准滑动窗口队列写法，语法正确，功能完整，口述与代码一致；时间复杂度为均摊 O(1)，可读性和注释都较好。


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
我会用递归的方式处理窗口更新。每进来一个新数据，我递归检查队首元素是不是过期，如果过期就删掉，然后继续递归，直到窗口内的数据都有效为止。

模拟候选人代码：
from collections import deque

def update_window(window_queue, new_time, new_value, window_size):
    window_queue.append((new_time, new_value))

    while window_queue and new_time - window_queue[0][0] > window_size:
        window_queue.popleft()

    return window_queue

备注：
代码语法正确且功能实现，但口述说“递归处理”，代码实际是 while 循环，因此 asr_match=0。


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
我会把每条流式数据按 (时间戳, 值) 的形式放进队列里。新数据入队之后，持续检查队首是否过期，如果当前时间减去队首时间大于窗口大小，就从队首弹出。这样窗口中始终只保留有效数据，时间复杂度是均摊 O(1)。

模拟候选人代码：
from collections import deque

def update_window(window_queue, new_time, new_value, window_size):
    window_queue.append((new_time, new_value))

    while window_queue and new_time - window_queue[0][0] > window_size
        window_queue.popleft()

    return window_queue



备注：
逻辑上是正确的滑动窗口队列方案，且与口述一致，但 while 条件后缺少冒号，属于语法错误，无法运行。

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
我会先把新数据放入队列，然后把所有已经过期的数据从队首移除，只保留当前窗口范围内的数据。也就是说，更新之后队列里应该只剩下有效元素。
模拟候选人代码：
from collections import deque

def update_window(window_queue, new_time, new_value, window_size):
    window_queue.append((new_time, new_value))

    if window_queue and new_time - window_queue[0][0] > window_size:
        window_queue.popleft()

    return window_queue

备注：
语法正确，但功能未完全实现。因为这里只删掉了一个过期元素，如果连续有多个过期元素，会残留错误数据。口述和代码的目标一致，但实现不完整。


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
我准备先把队列里的数据按数值大小排序，然后每次保留前几个最大的值，这样可以把窗口中有用的数据留下来，旧数据自然就会被替换掉。


模拟候选人代码：
def update_window(window_queue, new_time, new_value, window_size):
    window_queue.append((new_time, new_value))

    if len(window_queue) > window_size:
        window_queue.pop(0)

    return window_queue

备注：
代码语法正确，但没有按照“时间过期”删除元素，只是按长度裁剪，功能不正确；口述说的是“排序保留大值”，代码实际是“按长度弹出头部”，两者也不一致。


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
我会先把新数据加入队列，然后检查队首元素是否过期。如果过期，就从队首删除，直到队列里只剩窗口内的数据。这样更新之后队列就是当前有效窗口。


模拟候选人代码：
from collections import deque

def update_window(window_queue, new_time, new_value, window_size):
    window_queue.append((new_time, new_value))

    while window_queue and new_time - window_queue[0][0] > window_size
        window_queue.pop()

    return window_queue

备注：
while 后缺少冒号，存在语法错误；同时删除时用了 pop()，删除的是队尾而不是队首，功能也不正确。口述和代码都围绕“删除过期元素”这一逻辑展开，是一致的。


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
我会每次都重新遍历整个数据流，把窗口范围内的数据重新筛选出来，不一定依赖队列头删这种方式，虽然会慢一些，但实现比较直接。


模拟候选人代码：
from collections import deque

def update_window(window_queue, new_time, new_value, window_size):
    window_queue.append((new_time, new_value))

    while window_queue and new_time - window_queue[0][0] > window_size
        window_queue.popleft()

    return window_queue

备注：
代码逻辑上其实是正确的队列滑动窗口方案，但 while 后缺少冒号，属于语法错误；同时口述说的是“重新遍历全部数据筛选”，和代码逻辑不一致。


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
我会用队列保存窗口内的数据，新数据来了以后先入队，再不断移除队首中过期的数据。每个元素最多只会进出一次，所以时间复杂度还是均摊 O(1)。不过我这里为了方便，额外做了一次数组拷贝，空间上不是最优。


模拟候选人代码：
from collections import deque

def f(a, b, x, y):
    a.append((b, x))

    # 移除过期数据
    while a and b - a[0][0] > y:
        a.popleft()

    z = list(a)
    return z

备注：
功能实现正确，时间复杂度仍然是均摊 O(1)；但返回前做了额外拷贝，空间复杂度非最优。变量名如 a、b、x、y、z 比较混乱，可读性差。不过注释是有的。


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
我这里会先把新数据加进去，然后每次都重新扫描整个列表，把还在时间窗口内的数据重新放到一个新列表中，最后再替换原来的队列。这样能实现窗口更新，但每次更新都要重新遍历和重建结构，时间复杂度是 O(n)，空间复杂度也是 O(n)。


模拟候选人代码：
def a(x, t, v, w):
    x.append((t, v))
    y = []
    for i in x:
        if t - i[0] <= w:
            y.append(i)
    x[:] = y
    return x

备注：
代码语法正确，功能正确，口述与代码一致；但每次都重建列表，时间复杂度不是最优，空间复杂度也不是最优；变量命名混乱，且没有注释。




