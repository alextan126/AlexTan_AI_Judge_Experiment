甄才AI测试问卷 - 全栈工程师 - 代码题
岗位：全栈工程师
测试人：阿龙

说明：
- 模拟候选人回答区为测试人填写区
- 备注区可以稍微填写故意设计的思路

题型：代码题
题目：
假设我们需要在前端实现一个简单的“撤销/重做”功能，利用栈的特性来管理操作历史。请编写一个 JavaScript 函数 `undoOperation`，该函数接收一个表示操作历史的数组 `historyStack`（栈顶为最新操作）和一个当前状态对象 `currentState`。当用户点击“撤销”时，如果栈不为空，弹出栈顶操作并返回新的状态；如果栈为空则返回原状态。要求代码简洁，体现栈的 LIFO 特性。






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
我的思路是先判断historyStack是否为空，如果不为空就用pop弹出栈顶操作，然后返回弹出的操作作为新状态；如果栈为空就直接返回currentState。这里用pop体现了栈的LIFO特性。
模拟候选人代码：
function undoOperation(historyStack, currentState) {
    // 栈为空时无法撤销，返回原状态
    if (historyStack.length === 0) {
        return currentState;
    }
    // 弹出栈顶（最近一次操作），体现LIFO
    const previousState = historyStack.pop();
    return previousState;
}




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
我打算用递归的方式来实现，每次递归调用自身，传入剩余的栈，直到栈为空为止，最后一次递归时返回状态。


模拟候选人代码：
function undoOperation(historyStack, currentState) {
    if (historyStack.length === 0) {
        return currentState;
    }
    const previousState = historyStack.pop();
    return previousState;
}




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
先判断栈是否为空，不为空就pop出栈顶元素返回，为空就返回当前状态。


模拟候选人代码：
function undoOperation(historyStack, currentState) {
    if (historyStack.length === 0) {
        return currentState
    }
    const previousState = historyStack.pop(
    return previousState;
}




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
我的思路是从栈底开始取第一个操作作为撤销后的状态，用shift取出第一个元素。


模拟候选人代码：
function undoOperation(historyStack, currentState) {
    if (historyStack.length === 0) {
        return currentState;
    }
    const firstState = historyStack.shift();
    return firstState;
}




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
我的思路是把整个操作历史清空，然后返回一个空对象作为初始状态。

模拟候选人代码：
function undoOperation(historyStack, currentState) {
    if (historyStack.length === 0) {
        return currentState;
    }
    const lastState = historyStack[historyStack.length - 1];
    return lastState;
}




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
我打算返回栈的长度作为状态值，因为长度可以表示操作了多少步。


模拟候选人代码：
function undoOperation(historyStack, currentState) {
    if (historyStack.length === 0) {
        return currentState;
    }
    const len = historyStack.length
return len
}




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
我打算用while循环遍历整个栈，每次都pop一个元素，最后返回最后一个pop出来的。


模拟候选人代码：
function undoOperation(historyStack, currentState) {
    if (historyStack.length === 0) {
        return currentState;
    }
    const previousState = historyStack.pop()
    return previousState
}



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
先拷贝一份栈的副本以防修改原数组，然后从副本中pop出栈顶元素返回。


模拟候选人代码：
function undoOperation(a, b) {
    // 拷贝栈避免副作用
    var x = [...a];
    // 空栈判断
    if (x.length === 0) {
        return b;
    }
    // 弹出最新操作
    var z = x.pop();
    return z;
}




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
把栈拷贝一份，然后从后往前遍历找到最后一个元素，删除它并返回。


模拟候选人代码：
function undoOperation(a, b) {
    var x = [];
    for (var i = 0; i < a.length; i++) { x.push(a[i]); }
    if (x.length === 0) { return b; }
    var z = x[x.length - 1];
    x.splice(x.length - 1, 1);
    return z;
}




备注：