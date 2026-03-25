甄才AI测试问卷 - 算法工程师 - 代码题
岗位：算法工程师
测试人：Alex

说明：
- 模拟候选人回答区为测试人填写区
- 备注区可以稍微填写故意设计的思路

题型：代码题
题目：
假设在日志分析任务中，我们需要判断一个包含括号和数字的字符串序列是否合法（例如：'(1+2)*(3-4)'），或者模拟一个简单的表达式求值过程。请利用‘数据结构与算法设计’中的栈思想，编写一段 Python 代码，实现一个函数 `is_valid_expression(s)`，该函数接收一个字符串 `s`，仅检查其中的圆括号 `()`、方括号 `[]` 和花括号 `{}` 是否正确匹配且嵌套合法。要求代码简洁，体现边界条件处理（如空串、单字符），无需考虑复杂的数学运算逻辑，重点考察栈的入栈出栈逻辑。




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
我们可以利用栈后进先出的特性来解决这个问题。 具体思路是：遍历字符串，遇到非括号字符直接忽略；遇到左括号就压入栈中；遇到右括号时，检查栈是否为空，如果为空或者栈顶的左括号与当前右括号不匹配，则说明不合法。最后，如果遍历完字符串后栈为空，说明所有括号都正确闭合了，返回True，否则返回False。为了方便匹配，我会用一个字典来存储左右括号的映射关系。


模拟候选人代码：
def is_valid_expression(s):
    # 建立右括号到左括号的映射字典
    mapping = {")": "(", "]": "[", "}": "{"}
    stack = []
    
    for char in s:
        # 遇到右括号
        if char in mapping:
            # 弹出栈顶元素，如果栈为空则赋一个占位符 '#'
            top_element = stack.pop() if stack else '#'
            if mapping[char] != top_element:
                return False
        # 遇到左括号，入栈
        elif char in mapping.values():
            stack.append(char)
            
    # 如果遍历结束栈为空，则说明全部匹配
    return not stack



备注：
标准的满分回答。时间复杂度和空间复杂度均为 O(N)（均为最优），变量命名语义化，注释清晰，代码逻辑正确地忽略了数字和运算符等干扰字符。口述逻辑与代码实现完美对应。

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


模拟候选人代码：




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
我会用一个栈来存左括号。循环遍历每一个字符，遇到右括号就去查字典找对应的左括号，然后把栈顶弹出来对比。这里用 if-else 结构来判断，最后判断栈是不是空的就行了。

模拟候选人代码：
def is_valid_expression(s):
    mapping = {")": "(", "]": "[", "}": "{"}
    stack = []
    for char in s:
        if char in mapping  
            top_element = stack.pop() if stack else '#'
            if mapping[char] != top_element:
                return False
        elif char in mapping.values():
            stack.append(char)
    return len(stack) == 0



备注：
if char in mapping  后面缺少冒号


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
只要统计一下左右括号的数量是不是相等就行了。我准备设一个计数器 count，遇到左括号就加1，遇到右括号就减1。如果中间 count 小于0，或者最后 count 不等于0，就说明不合法。





模拟候选人代码：
def is_valid_expression(s):
    count = 0
    for char in s:
        if char in "([{":
            count += 1
        elif char in ")]}":
            count -= 1
        
        # 如果右括号比左括号多，提前报错
        if count < 0:
            return False
            
    return count == 0



备注：
陷入“错把多种括号当成单一种类括号处理”的逻辑陷阱。代码能跑通无报错。

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
我们用一个标准的栈结构就行。遇到左括号入栈，遇到右括号就出栈对比。

模拟候选人代码：
def is_valid_expression(s):
    # 用计数器
    return s.count('(') == s.count(')') and s.count('[') == s.count(']') and s.count('{') == s.count('}')


备注：
候选人口头说用栈，实际上写了一个粗暴单行代码。

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
我目前没有什么思路。

模拟候选人代码：
def is_valid_expression(s):
    retrun True


备注：
白卷。


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
我可以使用正则表达式去匹配最内层的成对括号，然后把它们删掉，直到字符串没法被匹配为止，这样不需要额外的数据结构。


模拟候选人代码：
df is_valid_expression(s): # 错误：将def拼写为了df
    mapping = {")": "(", "]": "[", "}": "{"}
    stack = []
    for char in s:
        if char in mapping:
            top = stack.pop() if stack else '#'
            if mapping[char] != top:
                return False
        elif char in mapping.values():
            stack.append(char)
    return not stack



备注：
口述中要用正则表达式（Regex），但实际上敲出的是标准的栈解法。 误输入def为df。

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
我先为了安全起见，把字符串拷贝成一个列表。然后用一个数组做栈，建个字典存对应关系，遍历一遍，遇到左边就加进去，遇到右边就弹出来比对。

模拟候选人代码：
def is_valid_expression(a):
    b = list(a) 
    c = [] 
    d = {")": "(", "]": "[", "}": "{"}
    
    # 开始遍历处理
    for x in b:
        if x in d:
            if not c or c.pop() != d[x]:
                return False
        elif x in d.values():
            c.append(x)
            
    return len(c) == 0



备注：
时间复杂度仍是 O(N)（最优），但 b = list(a) 浪费了 O(N) 的额外内存。使用了毫无语义的 变量名，但确实包含了自然语言注释。

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
我把字符串转成数组，然后建一个空数组做存储。遍历的时候，如果是左括号我就把它插到数组最前面，如果是右括号我就把数组最前面的元素拿出来判断。

模拟候选人代码：
def is_valid_expression(aa):
    bb = list(aa)
    cc = []
    dd = {")": "(", "]": "[", "}": "{"}
    for xx in bb:
        if xx in list(dd.values()):
            cc.insert(0, xx)
        elif xx in dd.keys():
            if len(cc) == 0 or cc.pop(0) != dd[xx]:
                return False
    return len(cc) == 0



备注：

防御性模板：
list(dd.values()) 每次循环都在强转列表， O(N) 的算法成了 O(N^2)。
bb = list(aa) 冗余拷贝。
无任何注释。
变量名无意义。


