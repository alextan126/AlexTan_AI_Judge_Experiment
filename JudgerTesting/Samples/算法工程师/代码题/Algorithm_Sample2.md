甄才AI测试问卷 - 算法工程师 - 代码题
岗位：算法工程师
测试人：徐博研

说明：
- 模拟候选人回答区为测试人填写区
- 备注区可以稍微填写故意设计的思路

题型：代码题
题目：
假设你需要编写一个 Python 函数来模拟深度学习框架中的“梯度裁剪”逻辑，防止深层网络训练时的梯度爆炸。已知梯度是一个列表 `gradients`，设定最大范数阈值 `max_norm`。请实现一个函数，当梯度的 L2 范数超过阈值时，将所有梯度按比例缩放至阈值范围内；否则保持原样。要求代码简洁，体现对向量运算的理解，无需引入外部库，仅使用基础数学运算即可。

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
我会先计算梯度列表的 L2 范数，也就是先把每个梯度平方求和，再开平方。如果这个范数超过 max_norm，就计算一个缩放系数 scale = max_norm / norm，然后把所有梯度都乘上这个系数；如果没有超过阈值，就直接返回原梯度。这样只需要遍历两次数组，时间复杂度是 O(n)，空间复杂度如果原地修改就是 O(1)。



模拟候选人代码：
def clip_gradients(gradients, max_norm):
    # 计算梯度的 L2 范数平方和
    squared_sum = 0.0
    for grad in gradients:
        squared_sum += grad * grad

    # 开平方得到 L2 范数
    norm = squared_sum ** 0.5

    # 如果范数未超过阈值，直接返回
    if norm <= max_norm or norm == 0:
        return gradients

    # 计算统一缩放比例
    scale = max_norm / norm

    # 原地缩放，节省额外空间
    for i in range(len(gradients)):
        gradients[i] *= scale

    return gradients

备注：
标准正确实现，口述与代码一致，时间复杂度 O(n)、空间复杂度 O(1)，变量命名和注释都较清晰。



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
我会用递归来实现梯度裁剪。先递归地计算整个列表的平方和，再递归地把每个元素按比例缩放，这样可以把逻辑拆得比较清楚。
模拟候选人代码：
def clip_gradients(gradients, max_norm):
    squared_sum = 0.0
    for grad in gradients:
        squared_sum += grad * grad

    norm = squared_sum ** 0.5

    if norm <= max_norm or norm == 0:
        return gradients

    scale = max_norm / norm
    for i in range(len(gradients)):
        gradients[i] *= scale

    return gradients
备注：
代码功能正确、语法正确，但口述说“用递归”，代码实际是普通循环实现，因此 asr_match=0。



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
我先计算梯度列表的 L2 范数，如果范数超过阈值，就求出统一的缩放比例，然后把每个梯度都乘上这个比例。这样所有梯度的相对方向保持不变，只是整体长度被限制到 max_norm 以内。


模拟候选人代码：
def clip_gradients(gradients, max_norm):
    squared_sum = 0.0
    for grad in gradients:
        squared_sum += grad * grad

    norm = squared_sum ** 0.5

    if norm <= max_norm or norm == 0:
        return gradients

    scale = max_norm / norm

    for i in range(len(gradients))
        gradients[i] *= scale

    return gradients

备注：
整体逻辑是正确的梯度裁剪思路，且与口述一致，但 for i in range(len(gradients)) 后缺少冒号，代码无法运行，属于语法错误。


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
我会先算出梯度的 L2 范数，如果超过阈值，就按 max_norm / norm 的比例去缩放所有梯度，否则保持不变。也就是说，只有总范数超限时才会整体缩放。

模拟候选人代码：
def clip_gradients(gradients, max_norm):
    squared_sum = 0.0
    for grad in gradients:
        squared_sum += grad * grad

    norm = squared_sum ** 0.5

    if norm <= max_norm or norm == 0:
        return gradients

    scale = max_norm / norm

    gradients[0] *= scale
    return gradients

备注：
语法正确，但只缩放了第一个梯度，没有实现“所有梯度按比例缩放”的要求，因此功能不正确。口述和代码的核心意图一致，都是在做整体缩放，只是代码实现残缺。


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
我打算先把梯度从小到大排序，然后如果最大的梯度超过阈值，就把超出的部分直接截断到阈值。这样可以快速防止梯度爆炸。


模拟候选人代码：
def clip_gradients(gradients, max_norm):
    total = 0.0
    for g in gradients:
        total += g

    if total > max_norm:
        return [max_norm for _ in gradients]
    return gradients



备注：
代码语法正确，但功能不对：它既没有计算 L2 范数，也没有按比例缩放；口述说的是“排序+截断最大值”，代码实际是“求和后全部改成阈值”，两者也不一致。


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
我这里的思路是先算出梯度的 L2 范数，如果范数超过阈值，就用 max_norm / norm 作为缩放系数，把每个梯度都乘上这个比例。否则就直接返回原列表。


模拟候选人代码：
def clip_gradients(gradients, max_norm):
    squared_sum = 0.0
    for grad in gradients:
        squared_sum += grad * grad

    norm = squared_sum ** 0.5

    if norm <= max_norm or norm == 0
        return gradients

    scale = max_norm / norm

    for i in range(len(gradients)):
        gradients[i] = gradients[i] + scale

    return gradients


备注：
if norm <= max_norm or norm == 0 后缺少冒号，语法错误；同时缩放时写成了 gradients[i] + scale 而不是乘法，功能也不正确。口述和代码都围绕“先算范数再统一处理梯度”，一致但实现错误。


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
我会直接把每个梯度单独和阈值比较，如果某个梯度绝对值超过阈值，就把它裁到 max_norm 或 -max_norm，这有点类似逐元素截断。


模拟候选人代码：
def clip_gradients(gradients, max_norm):
    squared_sum = 0.0
    for grad in gradients:
        squared_sum += grad * grad

    norm = squared_sum ** 0.5

    if norm <= max_norm or norm == 0:
        return gradients

    scale = max_norm / norm
    for i in range(len(gradients))
        gradients[i] *= scale

    return gradients



备注：
代码逻辑上其实是正确的整体 L2 范数裁剪，但 for i in range(len(gradients)) 后缺少冒号，存在语法错误；同时口述说的是“逐元素截断”，和代码逻辑不一致。


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
我会先计算整个梯度向量的 L2 范数，如果超过阈值，就算出统一的比例系数，然后把所有梯度整体缩放。为了写起来方便，我这里会额外复制一份数组再处理，不过整体时间复杂度还是线性的。


模拟候选人代码：
def f(a, b):
    c = a[:] 
    d = c[:] 
    x = 0.0

    # 计算平方和
    for y in d:
        x += y * y

    z = x ** 0.5

    # 如果未超阈值，直接返回复制后的列表
    if z <= b or z == 0:
        return d

    k = b / z

    # 按比例缩放所有元素
    for i in range(len(d)):
        d[i] *= k

    return d



备注：
功能正确，时间复杂度是 O(n)，但用了额外数组拷贝导致空间复杂度非最优；变量名 a、b、c、d、x、y、z、k 较混乱，可读性差。不过有注释，因此注释可读性通过。


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
我会先算梯度的 L2 范数，但我这里会用比较直接的方法，比如反复遍历、做中间数组，把平方值先存起来再处理。只要最后范数超了就统一缩放，否则保持原样。


模拟候选人代码：
def a(x, y):
    b = []
    for i in x:
        b.append(i * i)

    s = 0.0
    for j in b:
        s += j

    n = s ** 0.5

    if n <= y or n == 0:
        return x[:]

    k = y / n
    c = []
    for m in x:
        c.append(m * k)

    return c



备注：
代码语法正确，功能也正确，口述与代码一致；但先构造平方数组、再构造结果数组，空间复杂度非最优；需要多次遍历和中间存储，也不算时间最优写法；变量名混乱且没有注释。




