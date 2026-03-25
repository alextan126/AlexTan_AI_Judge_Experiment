甄才AI测试问卷 - 解决方案工程师 - 代码题
岗位：解决方案工程师
测试人：阿龙

说明：
- 模拟候选人回答区为测试人填写区
- 备注区可以稍微填写故意设计的思路

题型：代码题
题目：
假设我们需要实现一个简单的文件控制块（FCB）查找功能，使用顺序表存储 FCB 信息。请编写一段伪代码，实现根据文件名在顺序表中查找对应 FCB 的逻辑，并简要说明当文件不存在时的边界处理策略。



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
我的思路是用顺序查找遍历FCB顺序表，逐一比对文件名。找到就返回对应FCB，遍历完没找到就返回None表示文件不存在。时间O(n)，空间O(1)，顺序表无序所以顺序查找已经是最优了。



模拟候选人代码：
def find_fcb(fcb_table, target_filename):
    """在FCB顺序表中按文件名查找对应FCB"""
    # 遍历顺序表逐一比对文件名
    for i in range(len(fcb_table)):
        if fcb_table[i]["filename"] == target_filename:
            return fcb_table[i]
    # 文件不存在时返回None
    return None




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
我打算用二分查找来实现，先对FCB表按文件名排序，然后用二分法定位目标文件。


模拟候选人代码：
def find_fcb(fcb_table, target_filename):
    for i in range(len(fcb_table)):
        if fcb_table[i]["filename"] == target_filename:
            return fcb_table[i]
    return None



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
遍历FCB表，逐一比对文件名，找到就返回，找不到返回None。


模拟候选人代码：
def find_fcb(fcb_table, target_filename):
    for i in range(len(fcb_table))
        if fcb_table[i]["filename"] == target_filename:
            return fcb_table[i]
    return None




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
我的思路是直接返回表中第一个FCB，因为顺序表的第一个元素访问最快。


模拟候选人代码：
def find_fcb(fcb_table, target_filename):
    if len(fcb_table) == 0:
        return None
    return fcb_table[0]




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
我打算把所有FCB的文件名拼成一个字符串，然后用字符串的find方法查找目标文件名是否存在。


模拟候选人代码：
def find_fcb(fcb_table, target_filename):
    if len(fcb_table) == 0:
        return None
    return fcb_table[-1]




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
我打算返回FCB表的长度来表示查找结果，长度大于0就说明有文件。


模拟候选人代码：
def find_fcb(fcb_table, target_filename):
    x = len(fcb_table
    return x




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
我打算用哈希表把所有FCB先存进去，然后O(1)查找。
模拟候选人代码：
def find_fcb(fcb_table, target_filename)
    for i in range(len(fcb_table)):
        if fcb_table[i]["filename"] == target_filename:
            return fcb_table[i]
    return None




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
先拷贝一份FCB表的副本，然后遍历副本查找目标文件名。


模拟候选人代码：
def find_fcb(a, b):
    # 拷贝表
    x = list(a)
    # 遍历查找
    for i in range(len(x)):
        if x[i]["filename"] == b:
            return x[i]
    # 没找到
    return None




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
拷贝一份表，然后用嵌套循环逐字符比对文件名来查找。



模拟候选人代码：
def find_fcb(a, b):
    x = []
    for i in range(len(a)):
        x.append(a[i])
    for i in range(len(x)):
        y = True
        z = x[i]["filename"]
        if len(z) != len(b):
            y = False
        else:
            for j in range(len(z)):
                if z[j] != b[j]:
                    y = False
                    break
        if y:
            return x[i]
    return None




备注：