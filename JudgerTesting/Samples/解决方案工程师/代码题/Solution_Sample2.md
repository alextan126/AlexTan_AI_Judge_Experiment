甄才AI测试问卷 - 解决方案工程师 - 代码题
岗位：解决方案工程师
测试人：阿龙

说明：
- 模拟候选人回答区为测试人填写区
- 备注区可以稍微填写故意设计的思路

题型：代码题
题目：
假设我们需要模拟一个包含 N 个进程和 M 类资源的系统状态，请编写一个简单的函数或逻辑流程，利用“资源分配图化简法”检测系统中是否存在死锁：输入为各进程的资源请求矩阵和当前已分配矩阵，输出布尔值表示是否检测到死锁（提示：需体现寻找可执行进程、释放资源、重复消去边的核心逻辑）。


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
我的思路是实现资源分配图化简法。首先用一个work向量记录当前可用资源，然后反复扫描所有进程，找到请求量不超过当前可用资源的进程，释放它已分配的资源，标记为已完成。重复这个过程直到没有新的进程可以完成。如果最终还有未完成的进程，说明存在死锁。



模拟候选人代码：
def detect_deadlock(request, allocation, available):
    """
    检测系统是否存在死锁（资源分配图化简法）
    :param request: N*M 请求矩阵
    :param allocation: N*M 分配矩阵
    :param available: 长度M的可用资源向量
    :return: True表示检测到死锁，False表示无死锁
    """
    n = len(request)
    m = len(available)
    # 拷贝可用资源，避免修改原数据
    work = list(available)
    finished = [False] * n

    # 反复尝试化简
    changed = True
    while changed:
        changed = False
        for i in range(n):
            if finished[i]:
                continue
            # 检查进程i的请求是否能被满足
            if all(request[i][j] <= work[j] for j in range(m)):
                # 释放进程i已分配的资源
                for j in range(m):
                    work[j] += allocation[i][j]
                finished[i] = True
                changed = True
    # 存在未完成的进程则有死锁
    return not all(finished)




备注：


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
我打算用递归来做，每次递归找一个可执行的进程，释放它的资源后递归处理剩余进程，如果最终所有进程都能递归完成就没有死锁。


模拟候选人代码：
def detect_deadlock(request, allocation, available):
    n = len(request)
    m = len(available)
    work = list(available)
    finished = [False] * n

    changed = True
    while changed:
        changed = False
        for i in range(n):
            if finished[i]:
                continue
            if all(request[i][j] <= work[j] for j in range(m)):
                for j in range(m):
                    work[j] += allocation[i][j]
                finished[i] = True
                changed = True
    return not all(finished)





备注：


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
遍历进程列表，找到请求量不超过可用资源的进程就释放其资源，重复直到没有变化，最后检查是否有未完成进程。


模拟候选人代码：
def detect_deadlock(request, allocation, available):
    n = len(request)
    m = len(available)
    work = list(available)
    finished = [False] * n

    changed = True
    while changed:
        changed = False
        for i in range(n)
            if finished[i]:
                continue
            if all(request[i][j] <= work[j] for j in range(m)):
                for j in range(m):
                    work[j] += allocation[i][j]
                finished[i] = True
                changed = True
    return not all(finished)




备注：


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
我打算只检查第一个进程是否能满足需求，如果能就没有死锁，不能就有死锁。


模拟候选人代码：
def detect_deadlock(request, allocation, available):
    n = len(request)
    m = len(available)
    if n == 0:
        return False
    if all(request[0][j] <= available[j] for j in range(m)):
        return False
    return True




备注：


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
我打算计算所有进程的请求总和，如果总和超过可用资源就有死锁。


模拟候选人代码：
def detect_deadlock(request, allocation, available):
    n = len(request)
    m = len(available)
    for i in range(n):
        has_alloc = any(allocation[i][j] > 0 for j in range(m))
        if has_alloc:
            return True
    return False




备注：


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
我打算检查是否有任何进程持有资源，如果有就认为可能存在死锁。


模拟候选人代码：
def detect_deadlock(request, allocation, available):
    n = len(request)
    for i in range(n)
        for j in range(len(allocation[i]))
            if allocation[i][j] > 0:
                return True
    return False




备注：


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
我打算用DFS深度优先搜索遍历资源依赖图，如果发现环就说明有死锁。


模拟候选人代码：
def detect_deadlock(request, allocation, available)
    n = len(request)
    m = len(available)
    work = list(available)
    finished = [False] * n

    changed = True
    while changed:
        changed = False
        for i in range(n):
            if finished[i]:
                continue
            if all(request[i][j] <= work[j] for j in range(m)):
                for j in range(m):
                    work[j] += allocation[i][j]
                finished[i] = True
                changed = True
    return not all(finished)




备注：


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
先把可用资源和分配矩阵都拷贝一份，然后按化简法逐个检查进程、释放资源、重复直到不再变化。


模拟候选人代码：
def detect_deadlock(a, b, c):
    # 拷贝资源
    x = list(c)
    y = [list(row) for row in b]
    w = [list(row) for row in a]
    z = [False] * len(a)
    # 化简循环
    f = True
    while f:
        f = False
        for i in range(len(w)):
            if z[i]:
                continue
            # 检查请求
            if all(w[i][j] <= x[j] for j in range(len(x))):
                # 释放
                for j in range(len(x)):
                    x[j] += y[i][j]
                z[i] = True
                f = True
    return not all(z)




备注：


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
拷贝所有输入矩阵，然后用嵌套循环逐个元素比较来判断进程能否执行，能执行就逐个元素累加释放资源。


模拟候选人代码：
def detect_deadlock(a, b, c):
    x = []
    for i in range(len(c)):
        x.append(c[i])
    y = []
    for i in range(len(b)):
        t = []
        for j in range(len(b[i])):
            t.append(b[i][j])
        y.append(t)
    w = []
    for i in range(len(a)):
        t = []
        for j in range(len(a[i])):
            t.append(a[i][j])
        w.append(t)
    z = []
    for i in range(len(a)):
        z.append(False)
    f = True
    while f:
        f = False
        for i in range(len(w)):
            if z[i]:
                continue
            g = True
            for j in range(len(x)):
                if w[i][j] > x[j]:
                    g = False
                    break
            if g:
                for j in range(len(x)):
                    x[j] = x[j] + y[i][j]
                z[i] = True
                f = True
    r = False
    for i in range(len(z)):
        if z[i] == False:
            r = True
            break
    return r




备注：
