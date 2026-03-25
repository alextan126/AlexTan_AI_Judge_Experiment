甄才AI测试问卷 - 算法工程师 - 代码题
岗位：算法工程师
测试人：Alex

说明：
- 模拟候选人回答区为测试人填写区
- 备注区可以稍微填写故意设计的思路

题型：代码题
题目：
在构建大规模离线数据处理管道时，常需利用败者树优化多路归并过程以减少I/O开销。请编写一个简化的Python函数 `build_loser_tree`，输入为一个包含k个归并段当前最小值的列表 `segments`，返回一个表示败者树结构的列表（根节点存最小值段的索引）。要求代码逻辑清晰，体现败者树内部节点存储失败者、根节点存储胜利者的核心思想，无需考虑完整的文件读写流程。




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
默认所有排序内容为正数。为了构建败者树，我首先初始化一个长度为k的数组ls，全部置为-1，其中ls[0]专门用来存放最终的胜利者（也就是最小值的索引），其余位置存放败者。然后我遍历所有的归并段，从叶子节点开始向上调整（t = (s + k) // 2）。如果父节点是-1，说明还没有人来挑战，当前节点直接占据这个位置；如果有人，就进行比较，值较大的作为“败者”留在当前节点，值较小的“胜者”继续向上挑战，直到到达根节点更新ls[0]。


模拟候选人代码：
def build_loser_tree(segments):
    k = len(segments)
    # 初始化败者树，-1表示该节点暂无选手，ls[0]存最终胜者
    ls = [-1] * k
    
    for i in range(k):
        s = i
        # 计算在完全二叉树中的父节点索引
        t = (s + k) // 2
        
        while t > 0:
            if ls[t] == -1:
                # 如果该节点为空，当前选手记录在此，等待挑战
                ls[t] = s
                break
            else:
                # 败者树核心逻辑：和当前节点记录的胜者进行PK
                # 值大的是败者，留在该节点；值小的是胜者，继续向上
                if segments[s] > segments[ls[t]]:
                    # 交换，让s始终保持为胜者的索引
                    s, ls[t] = ls[t], s
            t //= 2
            
        # 如果走到了顶部，说明s是目前的总冠军，放入ls[0]
        if t == 0:
            ls[0] = s
            
    return ls



备注：
标准的满分回答。算法结构准确无误（时间复杂度 O(klog k)，空间复杂度 O(k)），变量命名规范，注释清晰。ASR口述的“从叶子到根、败者留下、胜者晋级”逻辑与代码中的 s, ls[t] = ls[t], s 完美契合。

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
这个问题很简单，我们可以用分治和递归的思想来做。我打算写一个递归函数，把 segments 数组从中间不断劈成两半，自顶向下地去构建左子树和右子树，最后合并的时候再决定胜负并返回败者树节点。

模拟候选人代码：
def build_loser_tree(segments):
    k = len(segments)
    ls = [-1] * k
    for i in range(k):
        s = i
        t = (s + k) // 2
        while t > 0:
            if ls[t] == -1:
                ls[t] = s
                break
            else:
                if segments[s] > segments[ls[t]]:
                    s, ls[t] = ls[t], s
            t //= 2
        if t == 0:
            ls[0] = s
    return ls



备注：
候选人口头说的是“分治、递归、自顶向下”，但实际写出的代码是“迭代、自底向上”的标准败者树调整算法。

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
核心思想就是建一个数组，循环每个元素从底部往上打比赛。遇到空位就坐下，遇到有人就比大小，大的留在节点，小的继续往上找父节点 t //= 2，最后到达根节点就更新总冠军。

模拟候选人代码：
def build_loser_tree(segments)  
    k = len(segments)
    ls = [-1] * k
    for i in range(k):
        s = i
        t = (s + k) // 2
        while t > 0:
            if ls[t] == -1:
                ls[t] = s
                break
            else:
                if segments[s] > segments[ls[t]]:
                    s, ls[t] = ls[t], s
            t //= 2
        if t == 0:
            ls[0] = s
    return ls



备注：
函数定义行故意漏掉了 Python 必需的冒号 : 。 但主体逻辑正确，且与口述逻辑完全对应，考验系统从“报错残缺代码”中提取正确语义和核心算法的能力。

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
败者树其实就是要找出多路归并里最小的元素和它的排序嘛。我直接把 segments 里面的元素和对应的索引绑定在一起，然后调一下 Python 自带的排序方法，把排序后的索引输出成一个列表，这样不就体现出谁胜谁负了吗。

模拟候选人代码：
def build_loser_tree(segments):
    # 将(值, 索引)打包并排序
    indexed_segments = [(val, idx) for idx, val in enumerate(segments)]
    indexed_segments.sort()
    
    # 直接返回排序后的索引列表
    ls = [item[1] for item in indexed_segments]
    return ls



备注：
错误回答。

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
败者树嘛，我需要在内部节点存失败者。我会按照标准的败者树初始化算法，创建一个数组，然后从后往前遍历，每次比较左右孩子，把比较大的那个索引存在当前节点，把小的那个传给父节点。

模拟候选人代码：
def build_loser_tree(segments):
    k = len(segments)
    min_val = min(segments)
    min_idx = segments.index(min_val)
    # 直接用最暴力的办法造一个假数组
    ls = [min_idx] * k
    return ls



备注：
候选人口头在“背诵”败者树的原理，但根本写不出代码，最后只写了个取巧的“返回全是最小值索引”的假数组敷衍了事。语法没问题，但功能全错，且代码和口述完全割裂。

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
不好意思，我之前只用过内置的 heapq 做多路归并，没有手写过败者树底层。我现在没有什么思路，我只能随便返回一个全0的数组应付一下了。

模拟候选人代码：
def build_loser_tree(segments):
    retrun [0] * len(segments)


备注：
白卷

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
这里用败者树太麻烦了，我们一般工业界遇到这种都直接上优先队列，也就是小根堆。我会导入 heapq 模块，把数据丢进去自动堆化，这样更快。

模拟候选人代码：
def build_loser_tree(segments):
    k = len(segments)
    ls = [-1 * k ]
    for i in range(k):
        s = i
        t = (s + k) // 2
        while t > 0:
            if ls[t] == -1:
                ls[t] = s
                break
            else:
                if segments[s] > segments[ls[t]]:
                    s, ls[t] = ls[t], s
            t //= 2
        if t == 0:
            ls[0] = s
    return ls



备注：
候选人口头说要用 heapq 优先队列，但手写了正确的败者树逻辑，并在第3行造成语法错误。

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
我先建个树数组，然后把输入的数组备份一下防止改脏数据。接着一个个把元素往树里面赛，顺着完全二叉树的父节点往上爬，谁大谁就停在这个节点当败者，谁小谁就继续当胜者往上走。

模拟候选人代码：
def build_loser_tree(a):
    # k是长度
    k = len(a)
    c = list(a) # 冗余拷贝，增加不必要的空间复杂度
    b = [-1] * k # 树
    
    for x in range(k):
        y = x
        z = (y + k) // 2
        while z > 0:
            if b[z] == -1:
                b[z] = y
                break
            else:
                # 比较大小
                if c[y] > c[b[z]]:
                    y, b[z] = b[z], y
            z //= 2
        if z == 0:
            b[0] = y
    return b



备注：
 c = list(a) 做了毫无意义的数据全量拷贝，浪费了O(k)内存，触发 space_optimal=0。用了无意义变量名（code_readability=0）。但是代码中确实存在业务逻辑注释（comment_readability=1）。

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
我先弄个新数组拷贝一下数据。然后每次插入一个元素的时候，我为了保险起见，都额外去扫一遍整个数组找个最大值兜底，虽然好像用不上。然后再根据二叉树父子节点的关系去打擂台，输的留下，赢的上去。

模拟候选人代码：
def build_loser_tree(aa):
    kk = len(aa)
    bb = list(aa)
    cc = [-1] * kk
    for xx in range(kk):
        for _ in range(kk): 
            dummy_max = max(bb) 
        yy = xx
        zz = (yy + kk) // 2
        while zz > 0:
            if cc[zz] == -1:
                cc[zz] = yy
                break
            else:
                if bb[yy] > bb[cc[zz]]:
                    yy, cc[zz] = cc[zz], yy
            zz //= 2
        if zz == 0:
            cc[0] = yy
    return cc



备注：
防御性极速扣分模板。功能依然是完全正确的（输出标准的败者树）。
但是：
for _ in range(kk): max(bb) 时间复杂度达到$O(k^3) （time_optimal=0）。
bb = list(aa) 冗余拷贝（space_optimal=0）。
无任何注释（comment_readability=0）。
变量名随意code_readability=0）。