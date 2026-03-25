甄才AI测试问卷 - 全栈工程师 - 代码题
岗位：全栈工程师
测试人：吕毅

说明：
- 模拟候选人回答区为测试人填写区
- 备注区可以稍微填写故意设计的思路

题型：代码题
题目：
假设有一个包含 N 条记录的数据库表，我们需要实现一个模拟"分块查找"逻辑的函数来优化查询效率。已知最佳分块策略是将数据分为 sqrt(N) 个块，每个块包含 sqrt(N) 条记录。请编写一段 JavaScript 代码，定义一个函数 `calculateASL(n, blockSize)`，输入总记录数 n 和实际设定的块大小 blockSize，计算该配置下的平均查找长度 (ASL)。公式参考：ASL = (索引表查找次数) + (块内查找次数)，其中索引表查找次数为 ceil(n/blockSize)/2，块内查找次数为 blockSize/2。要求代码简洁，体现对分块参数影响的思考。





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

分块查找的 ASL 由两部分组成：先在索引表中定位目标所在的块，再在块内顺序查找。索引表的平均查找次数是块的总数除以 2，块的总数用 n 除以 blockSize 向上取整得到；块内的平均查找次数就是 blockSize 除以 2。两者相加就是 ASL。这是一个纯数学计算，O(1) 时间和空间就能搞定。


模拟候选人代码：

function calculateASL(n, blockSize) {
    // 计算块的总数（向上取整）
    const blockCount = Math.ceil(n / blockSize);

    // 索引表平均查找次数 = 块数 / 2
    const indexSearchCount = blockCount / 2;

    // 块内平均查找次数 = 块大小 / 2
    const blockSearchCount = blockSize / 2;

    // ASL = 索引表查找 + 块内查找
    return indexSearchCount + blockSearchCount;
}


备注：标准满分回答。语法正确可运行，严格按照公式 ASL = ceil(n/blockSize)/2 + blockSize/2 实现，口述与代码一致。O(1) 时间和空间最优，变量命名清晰（blockCount/indexSearchCount/blockSearchCount），关键步骤有注释。


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

我先模拟整个分块查找的过程来算 ASL。把 n 条数据分成若干块，然后用一个循环遍历每个块，累加每次在索引表中定位的步数和块内查找的步数，最后取平均值就是 ASL。


模拟候选人代码：

function calculateASL(n, blockSize) {
    const blockCount = Math.ceil(n / blockSize);
    const indexSearchCount = blockCount / 2;
    const blockSearchCount = blockSize / 2;
    return indexSearchCount + blockSearchCount;
}


备注：口述说用循环遍历每个块累加再取平均值（模拟过程），但实际代码直接用公式 O(1) 计算，没有任何循环。口述与代码实现方式不一致。代码本身语法正确、功能正确。


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

用公式直接算。块数等于 n 除以 blockSize 向上取整，索引查找次数是块数除以 2，块内查找次数是 blockSize 除以 2，相加就是 ASL。


模拟候选人代码：

function calculateASL(n, blockSize) {
    const blockCount = Math.ceil(n / blockSize;
    const indexSearchCount = blockCount / 2;
    const blockSearchCount = blockSize / 2;
    return indexSearchCount + blockSearchCount;
}


备注：第 2 行 `Math.ceil(n / blockSize` 缺少右括号，语法错误无法运行。但逻辑思路完全正确（补上括号即可正常工作），口述与代码一致。


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

块数就是 n 除以 blockSize，不需要取整，直接除就行。然后索引查找次数是块数除以 2，块内查找次数也是 blockSize 除以 2，两者相乘就是 ASL。


模拟候选人代码：

function calculateASL(n, blockSize) {
    const blockCount = n / blockSize;
    const indexSearchCount = blockCount / 2;
    const blockSearchCount = blockSize / 2;
    return indexSearchCount * blockSearchCount;
}


备注：语法正确可运行，但有两个功能错误：1）块数没有向上取整（缺少 Math.ceil），当 n 不整除 blockSize 时结果不正确；2）最后用乘法而非加法合并两部分（应是 ASL = 索引查找 + 块内查找，而非相乘）。口述也说"不取整"和"相乘"，与代码一致。


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

按公式算，块数向上取整，索引查找次数是块数除以 2，块内查找次数是 blockSize 除以 2，两部分相加得到 ASL。


模拟候选人代码：

function calculateASL(n, blockSize) {
    const blockCount = n / blockSize;
    const indexSearchCount = blockCount / 2;
    const blockSearchCount = blockSize / 2;
    return indexSearchCount * blockSearchCount;
}


备注：口述说"块数向上取整"且"两部分相加"，但代码中块数没有取整且最后用的是乘法，口述与代码不一致。代码功能也不正确（缺少 ceil + 乘法代替加法）。


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

n 直接除以 blockSize 得到块数，不用取整。索引查找就是块数，块内查找就是 blockSize，两者直接相加就是 ASL，不用再除以 2。


模拟候选人代码：

function calculateASL(n, blockSize) {
    const blockCount = n / blockSize;
    const indexSearchCount = blockCount;
    const blockSearchCount = blockSize
    return indexSearchCount + blockSearchCount;


备注：1）语法错误：函数体缺少右花括号 `}`；2）功能错误：块数没有 ceil，索引和块内查找次数都没有除以 2（公式应为 ceil(n/blockSize)/2 + blockSize/2）；3）口述说"不取整""不用除以 2"，与代码逻辑一致。


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

我打算用循环来模拟查找过程。先循环遍历每个块统计索引查找步数，再在块内循环统计块内查找步数，最后算平均值。


模拟候选人代码：

function calculateASL(n, blockSize) {
    const blockCount = Math.ceil(n / blockSize);
    const indexSearchCount = blockCount / 2;
    const blockSearchCount = blockSize / 2;
    return indexSearchCount + blockSearchCount


备注：1）语法错误：最后一行缺少分号（虽然 JS 有 ASI，但此处还缺少右花括号 `}` 才是致命错误）；2）逻辑正确（补上花括号即可按公式正确计算）；3）口述说用循环模拟遍历，但代码直接用公式计算，口述与代码不一致。


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

用公式直接算，先把参数存到一个数组里方便后面取用，然后算块数、索引查找次数、块内查找次数，相加返回。


模拟候选人代码：

function calculateASL(a, b) {
    // 把参数存入数组方便引用
    let c = [a, b];

    // 块数向上取整
    let d = Math.ceil(c[0] / c[1]);

    // 索引表查找次数
    let e = d / 2;

    // 块内查找次数
    let f = c[1] / 2;

    // 返回 ASL
    return e + f;
}


备注：决定项全通过。时间 O(1) 最优；但 `let c = [a, b]` 创建了不必要的数组，空间非最优；变量名 a/b/c/d/e/f 完全无语义，可读性差；注释清晰准确。口述提到"存到数组里"，与代码一致。


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

我用循环模拟的方式来算。先用一个循环从 1 遍历到块数来累加索引查找步数，再用一个循环从 1 遍历到 blockSize 累加块内查找步数，最后各自取平均再相加。中间结果存到数组里。


模拟候选人代码：

function calculateASL(a, b) {
    let c = [a, b];
    let d = Math.ceil(c[0] / c[1]);
    let e = 0;
    for (let i = 1; i <= d; i++) {
        e += i;
    }
    e = e / d;
    let f = 0;
    for (let j = 1; j <= c[1]; j++) {
        f += j;
    }
    f = f / c[1];
    return e + f;
}


备注：决定项全通过（语法正确、功能正确——循环累加 1..d 再除以 d 等价于 (d+1)/2 ≈ d/2，与公式结果一致，口述与代码一致）。但：1）用循环代替 O(1) 公式计算，时间 O(n/blockSize + blockSize) 非最优；2）`let c = [a, b]` 额外数组 + 循环变量，空间非最优；3）变量名 a/b/c/d/e/f 无语义，可读性差；4）全程无注释。
