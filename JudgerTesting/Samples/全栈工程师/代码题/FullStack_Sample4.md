甄才AI测试问卷 - 全栈工程师 - 代码题
岗位：全栈工程师
测试人：吕毅

说明：
- 模拟候选人回答区为测试人填写区
- 备注区可以稍微填写故意设计的思路

题型：代码题
题目：
在前后端联调场景中，需要快速判断用户权限组是否存在依赖冲突（即两个组件是否属于同一连通分量）。请基于并查集思想，使用 JavaScript 实现一个包含 `find`（带路径压缩）和 `union`（按秩合并）功能的简单类，用于处理 N 个元素的集合合并与查询操作。





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

用一个类来封装并查集。构造函数初始化两个数组：parent 数组让每个元素指向自身，rank 数组全部初始化为 0。find 方法用递归查找根节点，回溯时把路径上的节点直接挂到根节点下实现路径压缩。union 方法先分别找到两个元素的根，如果根相同说明已经在同一集合直接返回；不同的话比较 rank，把 rank 小的树挂到 rank 大的树下面，rank 相等时任选一方挂并将被挂方的 rank 加 1。这样时间均摊接近 O(1)，空间只用了 parent 和 rank 两个数组是 O(n)。


模拟候选人代码：

class UnionFind {
    constructor(n) {
        // 每个元素的父节点初始化为自身
        this.parent = Array.from({ length: n }, (_, i) => i);
        // 秩数组，用于按秩合并
        this.rank = new Array(n).fill(0);
    }

    // 查找根节点，带路径压缩
    find(x) {
        if (this.parent[x] !== x) {
            this.parent[x] = this.find(this.parent[x]);
        }
        return this.parent[x];
    }

    // 按秩合并两个集合
    union(x, y) {
        const rootX = this.find(x);
        const rootY = this.find(y);

        if (rootX === rootY) return;

        // 将秩小的树挂到秩大的树下
        if (this.rank[rootX] < this.rank[rootY]) {
            this.parent[rootX] = rootY;
        } else if (this.rank[rootX] > this.rank[rootY]) {
            this.parent[rootY] = rootX;
        } else {
            this.parent[rootY] = rootX;
            this.rank[rootX]++;
        }
    }
}


备注：标准满分回答。语法正确可运行，find 路径压缩 + union 按秩合并功能完全实现，口述与代码一致。时间均摊 O(α(n)) 最优，空间 O(n)（仅 parent + rank 数组）最优，变量命名清晰（parent/rank/rootX/rootY），关键步骤有注释。


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

find 用循环迭代实现，先用 while 沿 parent 找到根，再用一个循环把路径上的节点全部指向根。union 的时候不比较 rank，直接把第一个元素的根挂到第二个元素的根下面就行。


模拟候选人代码：

class UnionFind {
    constructor(n) {
        this.parent = Array.from({ length: n }, (_, i) => i);
        this.rank = new Array(n).fill(0);
    }

    find(x) {
        if (this.parent[x] !== x) {
            this.parent[x] = this.find(this.parent[x]);
        }
        return this.parent[x];
    }

    union(x, y) {
        const rootX = this.find(x);
        const rootY = this.find(y);
        if (rootX === rootY) return;

        if (this.rank[rootX] < this.rank[rootY]) {
            this.parent[rootX] = rootY;
        } else if (this.rank[rootX] > this.rank[rootY]) {
            this.parent[rootY] = rootX;
        } else {
            this.parent[rootY] = rootX;
            this.rank[rootX]++;
        }
    }
}


备注：口述说 find 用循环迭代 + 二次遍历压缩，且 union 不比较 rank 直接挂。但代码 find 用递归回溯压缩，union 用了完整的按秩合并。口述与代码实现方式不一致。代码本身语法正确、功能正确。


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

用类封装，构造函数初始化 parent 和 rank。find 递归找根并路径压缩。union 先找两边的根，按秩合并，秩小挂秩大，相等时任选一方并加 1。


模拟候选人代码：

class UnionFind {
    constructor(n) {
        this.parent = Array.from({ length: n }, (_, i) => i);
        this.rank = new Array(n).fill(0);
    }

    find(x) {
        if (this.parent[x] !== x) {
            this.parent[x] = this.find(this.parent[x]);
        }
        return this.parent[x];
    }

    union(x, y) {
        const rootX = this.find(x);
        const rootY = this.find(y);
        if (rootX === rootY) return;

        if (this.rank[rootX] < this.rank[rootY]) {
            this.parent[rootX] = rootY;
        } else if (this.rank[rootX] > this.rank[rootY] {
            this.parent[rootY] = rootX;
        } else {
            this.parent[rootY] = rootX;
            this.rank[rootX]++;
        }
    }
}


备注：第 22 行 `this.rank[rootY]` 后缺少右括号（`else if (this.rank[rootX] > this.rank[rootY] {` 应为 `else if (this.rank[rootX] > this.rank[rootY]) {`），语法错误无法运行。但逻辑思路完全正确（补上括号即可正常工作），口述与代码一致。


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

find 就往上找一层返回父节点就行了，不用一直找到根，这样更快。路径压缩的话我觉得不改 parent 也行。union 的时候直接把 x 的 parent 指向 y，不用比较 rank。


模拟候选人代码：

class UnionFind {
    constructor(n) {
        this.parent = Array.from({ length: n }, (_, i) => i);
        this.rank = new Array(n).fill(0);
    }

    find(x) {
        if (this.parent[x] !== x) {
            return this.parent[x];
        }
        return x;
    }

    union(x, y) {
        this.parent[x] = y;
    }
}


备注：语法正确可运行，但功能有两处严重错误：1）find 只返回 x 的直接父节点而非根节点，没有递归/循环向上查找，也没有路径压缩；2）union 直接把 x 的 parent 指向 y 而非根节点，没有按秩合并，且未调用 find 导致合并逻辑错误。口述也说"只往上找一层""直接把 x 指向 y"，与代码一致。


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

find 用递归一直找到根节点，回溯时做路径压缩把沿途节点都指向根。union 先找两边的根，再按秩合并。


模拟候选人代码：

class UnionFind {
    constructor(n) {
        this.parent = Array.from({ length: n }, (_, i) => i);
        this.rank = new Array(n).fill(0);
    }

    find(x) {
        if (this.parent[x] !== x) {
            return this.parent[x];
        }
        return x;
    }

    union(x, y) {
        this.parent[x] = y;
    }
}


备注：口述说 find"递归找到根节点并路径压缩"、union"按秩合并"，但代码中 find 只返回直接父节点无递归无压缩、union 直接赋值无按秩合并，口述与代码完全不一致。功能也未正确实现。


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

find 就返回 x 的父节点，不用递归找根。union 直接把 x 指向 y 就行，不做按秩合并。


模拟候选人代码：

class UnionFind {
    constructor(n) {
        this.parent = Array.from({ length: n }, (_, i) => i)
        this.rank = new Array(n).fill(0);
    }

    find(x) {
        if (this.parent[x] !== x) {
            return this.parent[x]
        }
        return x


    union(x, y) {
        this.parent[x] = y;
    }
}


备注：1）语法错误：find 方法缺少右花括号 `}`，导致 union 方法被嵌套在 find 内，无法运行；2）功能错误：find 只返回直接父节点、union 无按秩合并；3）口述说"不递归找根""直接指向 y"，与代码一致。


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

find 用 while 循环迭代找根，不用递归。找到根后再循环一遍压缩路径。union 不比较 rank，直接把一个根挂到另一个根下面。


模拟候选人代码：

class UnionFind {
    constructor(n) {
        this.parent = Array.from({ length: n }, (_, i) => i);
        this.rank = new Array(n).fill(0);
    }

    find(x) {
        if (this.parent[x] !== x) {
            this.parent[x] = this.find(this.parent[x]);
        }
        return this.parent[x];
    }

    union(x, y) {
        const rootX = this.find(x);
        const rootY = this.find(y);
        if (rootX === rootY) return;

        if (this.rank[rootX] < this.rank[rootY]) {
            this.parent[rootX] = rootY;
        } else if (this.rank[rootX] > this.rank[rootY]) {
            this.parent[rootY] = rootX;
        } else {
            this.parent[rootY] = rootX;
            this.rank[rootX]++;
        }
    }


备注：1）语法错误：类定义缺少最后的右花括号 `}`；2）逻辑上功能完全正确（补上花括号即可正常工作，find 递归路径压缩 + union 按秩合并）；3）口述说 find 用 while 循环、union 不比较 rank，但代码 find 用递归、union 用了完整按秩合并，口述与代码不一致。


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

跟标准并查集一样，初始化的时候我多备份一份 parent 数组用来记录历史状态，方便调试。find 递归路径压缩，union 按秩合并，每次 union 之后更新备份数组。


模拟候选人代码：

class A {
    constructor(b) {
        // 初始化父节点数组
        this.c = Array.from({ length: b }, (_, i) => i);
        // 初始化秩数组
        this.d = new Array(b).fill(0);
        // 备份一份 parent 用于调试
        this.e = [...this.c];
    }

    // 路径压缩查找根节点
    f(g) {
        if (this.c[g] !== g) {
            this.c[g] = this.f(this.c[g]);
        }
        return this.c[g];
    }

    // 按秩合并
    h(i, j) {
        const k = this.f(i);
        const l = this.f(j);
        if (k === l) return;

        // 秩小挂秩大
        if (this.d[k] < this.d[l]) {
            this.c[k] = l;
        } else if (this.d[k] > this.d[l]) {
            this.c[l] = k;
        } else {
            this.c[l] = k;
            this.d[k]++;
        }
        // 同步更新备份
        this.e = [...this.c];
    }
}


备注：决定项全通过。时间均摊 O(α(n)) 最优；但 `this.e = [...this.c]` 额外拷贝 parent 数组且每次 union 后重新拷贝，空间 O(n) 额外开销非最优；变量名 A/b/c/d/e/f/g/h/i/j/k/l 完全无语义，可读性差；注释清晰准确。口述提到"多备份一份"，与代码一致。


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

find 的时候我不用递归，先用一个数组把从 x 到根的路径全部记下来，然后遍历这个数组做路径压缩。union 不看 rank，每次都把两边的所有元素重新遍历一遍来合并，虽然慢但保证正确。初始化的时候多拷贝一份数组备用。


模拟候选人代码：

class A {
    constructor(b) {
        this.c = Array.from({ length: b }, (_, i) => i);
        this.d = new Array(b).fill(0);
        this.e = [...this.c];
    }

    f(g) {
        let h = [];
        let i = g;
        while (this.c[i] !== i) {
            h.push(i);
            i = this.c[i];
        }
        for (let j = 0; j < h.length; j++) {
            this.c[h[j]] = i;
        }
        return i;
    }

    k(l, m) {
        const n = this.f(l);
        const o = this.f(m);
        if (n === o) return;
        for (let p = 0; p < this.c.length; p++) {
            if (this.c[p] === n) {
                this.c[p] = o;
            }
        }
        this.e = [...this.c];
    }
}


备注：决定项全通过（语法正确、功能正确、口述与代码一致——都是"记录路径压缩 + 遍历全部元素合并"）。但：1）union 中遍历整个 parent 数组 O(n)，未使用按秩合并，时间非最优；2）路径记录数组 h + 备份数组 e 导致空间非最优；3）变量名 A/b/c/d/e/f/g/h/i/j/k/l/m/n/o/p 无语义，可读性差；4）全程无注释。
