甄才AI测试问卷 - 解决方案工程师 - 代码题
岗位：解决方案工程师
测试人：老张
说明：
模拟候选人回答区为测试人填写区
备注区可以稍微填写故意设计的思路
题型：代码题
题目：
假设你需要为一个任务调度系统设计核心逻辑，该系统包含 N 个任务节点和 M 个依赖关系（有向图），任务是解决“任务死锁检测”问题。请编写一个简化的 C/C++ 函数，输入为表示任务依赖关系的邻接表（Adjacency List），输出为布尔值：如果图中存在环（即任务互相等待导致死锁）返回 true，否则返回 false。只需写出核心递归或迭代逻辑，无需完整可执行代码
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
建模逻辑：将任务视为图的顶点（Vertex），任务间的依赖关系视为有向边（Edge）。若 A 依赖 B，则存在一条从 B 指向 A 的边（B 完成后 A 才能开始）。核心算法：采用 Kahn 算法（广度优先搜索 BFS）。统计入度：记录每个任务节点的入度（即该任务依赖的前置任务数量）。初始化队列：将所有入度为 0 的节点（无依赖任务）放入队列。拓扑排序遍历：不断从队列中取出节点，并计数。遍历该节点的所有邻接节点（受其影响的后续任务），将其入度减 1。如果某个邻接节点的入度减为 0，则将其加入队列。死锁判断：如果最终计数处理的任务数量等于总任务数 $N$，说明不存在环，无死锁。如果计数小于 $N$，说明图中存在环（任务互相等待），返回 true（检测到死锁）。复杂度分析：时间复杂度：$O(N + M)$，其中 $N$ 是任务数，$M$ 是依赖关系数。每个节点和每条边仅被访问一次。空间复杂度：$O(N + M)$，用于存储邻接表和入度数组。
模拟候选人代码：
#include <vector>
#include <queue>

/**
 * 任务死锁检测函数
 * @param n 任务总数 (节点 0 到 n-1)
 * @param adj 邻接表，adj[u] 存储了所有依赖任务 u 的后续任务 v
 * @return bool 如果存在死锁(环)返回 true，否则返回 false
 */
bool hasDeadlock(int n, const std::vector<std::vector<int>>& adj) {
    std::vector<int> in_degree(n, 0);
    
    // 1. 统计所有节点的入度
    for (int u = 0; u < n; ++u) {
        for (int v : adj[u]) {
            in_degree[v]++;
        }
    }

    // 2. 将所有入度为 0 的节点入队 (即没有任何前置依赖的任务)
    std::queue<int> q;
    for (int i = 0; i < n; ++i) {
        if (in_degree[i] == 0) {
            q.push(i);
        }
    }

    int processed_count = 0; // 记录已成功调度的任务数

    // 3. 执行拓扑排序 (BFS)
    while (!q.empty()) {
        int u = q.front();
        q.pop();
        processed_count++;

        // 遍历当前任务的后继节点
        for (int v : adj[u]) {
            // 后继节点的前置任务完成，入度减 1
            if (--in_degree[v] == 0) {
                q.push(v);
            }
        }
    }

    // 4. 判断逻辑：如果处理任务数不等于总数，说明存在环，即发生死锁
    return processed_count != n;
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
为了检测任务调度系统中的死锁，我采用了深度优先搜索（DFS）的递归回溯算法。

递归逻辑：我定义了一个递归函数，通过传入当前的节点索引和访问状态数组。

状态标记：在递归过程中，我会将当前路径上的节点标记为“访问中”，如果递归遇到已经处于“访问中”的节点，则说明发现了环。

回溯：当递归退出当前分支时，我会进行状态回溯，将标记清除，以保证不影响其他路径的检测。
模拟候选人代码：
#include <vector>
#include <queue>

// 核心函数：检测任务死锁
bool hasDeadlock(int n, const std::vector<std::vector<int>>& adj) {
    std::vector<int> in_degree(n, 0);
    for (int i = 0; i < n; ++i) {
        for (int v : adj[i]) {
            in_degree[v]++;
        }
    }

    std::queue<int> q;
    for (int i = 0; i < n; ++i) {
        if (in_degree[i] == 0) q.push(i);
    }

    int count = 0;
    // 此处实际逻辑为 BFS 迭代，并非口述中所说的 DFS 递归
    while (!q.empty()) {
        int u = q.front();
        q.pop();
        count++;

        for (int v : adj[u]) {
            if (--in_degree[v] == 0) {
                q.push(v);
            }
        }
    }

    // 若 count != n 则存在环（死锁）
    return count != n;
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
算法选择：我使用 深度优先遍历（DFS） 配合 染色法 来检测任务依赖中的环。

状态定义：

0 (Unvisited)：节点尚未被探索。

1 (Visiting)：节点正在当前递归路径中，如果再次遇到此状态的节点，说明存在环（死锁）。

2 (Visited)：节点及其所有子节点已探索完毕。

递归执行：对每个节点进行 DFS。进入节点时设为状态 1，递归结束后设为状态 2。如果在递归过程中访问到状态为 1 的节点，立即返回 true。
模拟候选人代码：
#include <vector>

// 检查是否存在死锁的递归辅助函数
bool hasCycle(int u, std::vector<int>& state, const std::vector<std::vector<int>>& adj) {
    state[u] = 1; // 标记为正在访问

    for (int v : adj[u]) {
        if (state[v] == 1) return true; // 发现环
        if (state[v] == 0) {
            // 【语法错误 1】: 下行缺少左括号，且 if 语句后面缺少花括号或逻辑结构错误
            if hasCycle(v, state, adj) 
                return true;
        }
    }

    state[u] = 2; // 标记为已访问完成
    return false;
// 【语法错误 2】: 缺少函数结束的右大括号 }

bool hasDeadlock(int n, const std::vector<std::vector<int>>& adj) {
    std::vector<int> state(n, 0); 
    
    for (int i = 0; i < n; ++i) {
        if (state[i] == 0) {
            // 【语法错误 3】: 语句末尾缺少分号
            if (hasCycle(i, state, adj)) return true
        }
    }
    return false;
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
核心逻辑：我通过 DFS（深度优先搜索） 配合 访问标记数组 来检测死锁。

递归策略：对于每个任务，我递归遍历其依赖的所有子任务。

判定条件：我使用一个布尔数组 visited。在遍历过程中，如果发现当前节点已经被访问过（即 visited[u] == true），则说明我们回到了之前走过的节点，判定为存在环（死锁）。
模拟候选人代码：
#include <vector>

// 错误的 DFS 辅助函数
bool dfs(int u, std::vector<bool>& visited, const std::vector<std::vector<int>>& adj) {
    if (visited[u]) return true; // 错误点：在有向图中，已访问不代表有环

    visited[u] = true;
    for (int v : adj[u]) {
        if (dfs(v, visited, adj)) return true;
    }
    return false;
}

/**
 * 任务死锁检测（存在逻辑缺陷版）
 */
bool hasDeadlock(int n, const std::vector<std::vector<int>>& adj) {
    std::vector<bool> visited(n, false);

    for (int i = 0; i < n; ++i) {
        // 每次从新节点出发时，并没有清除 visited 状态或区分路径状态
        if (!visited[i]) {
            if (dfs(i, visited, adj)) return true;
        }
    }
    return false;
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
核心逻辑：我采用的是基于 出度（Out-degree）的贪心算法 来检测死锁。

算法过程：我会先计算所有节点的出度。如果一个节点的出度为 0，说明它是终点，不可能是死锁的一部分。我会递归地移除这些节点。

判定条件：如果最后剩余的节点集合中，所有节点的出度都大于 1，则判定存在死锁。
模拟候选人代码：
#include <vector>

/**
 * 任务死锁检测（语法正确但逻辑与口述双重错误版）
 */
bool hasDeadlock(int n, const std::vector<std::vector<int>>& adj) {
    std::vector<int> degree_count(n, 0);

    // 实际逻辑：统计入度
    for (int i = 0; i < n; ++i) {
        for (int v : adj[i]) {
            degree_count[v]++;
        }
    }

    // 错误逻辑：简单地认为入度超过 1 就是死锁
    for (int i = 0; i < n; ++i) {
        if (degree_count[i] > 1) { 
            return true; 
        }
    }

    return false;
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
核心逻辑：我通过统计图中边的总数来判断是否存在死锁。算法过程：我遍历整个邻接表，计算出所有的依赖关系数量。判定条件：在一个任务系统中，如果依赖关系的数量 $M$ 超过了任务节点的数量 $N$，那么根据抽屉原理，它们一定会形成一个环。所以我只要判断 edge_count > node_count 即可。
模拟候选人代码：
#include <vector>

bool hasDeadlock(int n, const std::vector<std::vector<int>>& adj) {
    int edge_count = 0  // 【语法错误 1】: 缺少分号

    // 逻辑：统计边数（与口述一致，但功能错误）
    for (int i = 0; i < n; ++i) {
        for (int v : adj[i]) {
            edge_count++
        }
    }

    // 【语法错误 2】: 变量 node_count 未声明，直接使用
    // 【语法错误 3】: if 语句缺少圆括号
    if edge_count > node_count 
        return true;
    } 
    // 【语法错误 4】: 缺少对应的左大括号或结构混乱

    return false;
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
核心逻辑：我计划使用 Kahn 算法，这是一种基于 入度 的广度优先搜索。

算法过程：我会统计每个任务的入度，并将入度为 0 的节点放入队列。

判定条件：通过不断弹出队列节点并削减其邻居的入度，如果最后处理的节点数小于总数，则存在环。
模拟候选人代码：
#include <vector>

// 实际使用 DFS 逻辑，与口述的入度逻辑不符
bool check(int u, vector<int>& s, const vector<vector<int>>& a) { // 【语法错误 1】: 未使用 std:: 前缀
    s[u] = 1;
    for (int v : a[u]) {
        if (s[v] == 1) return true;
        if (s[v] == 0 && check(v, s, a)) return true;
    }
    s[u] = 2;
    return false
} // 【语法错误 2】: 缺少分号

bool hasDeadlock(int n, const std::vector<std::vector<int>>& adj) {
    std::vector<int> state(n, 0);
    for (int i = 0; i < n; ++i) {
        // 【语法错误 3】: check 函数参数传递类型不匹配或未在当前作用域完全声明
        if (state[i] == 0 && check(i, state, adj)) return true;
    }
    return false;
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
核心算法：我使用的是 Kahn 算法 进行拓扑排序来检测死锁。

逻辑流程：首先统计每个节点的入度，把入度为 0 的点放进队列。然后不断取出节点，更新它指向的节点的入度。

判定依据：如果最后处理过的节点数量和总任务数相等，就没有死锁。为了保险，我会在处理前先备份一份邻接表，防止修改原始数据。
模拟候选人代码：
#include <vector>
#include <queue>

// 核心函数：检测死锁
bool hasDeadlock(int n, const std::vector<std::vector<int>>& a) {
    // 空间非最优：额外备份了整个邻接表，增加了 O(M) 的空间开销
    std::vector<std::vector<int>> b = a; 
    
    std::vector<int> c(n, 0); // c 代表入度数组
    for (int i = 0; i < n; ++i) {
        for (int x : b[i]) {
            c[x]++;
        }
    }

    std::queue<int> q; // q 是待处理队列
    for (int i = 0; i < n; ++i) {
        if (c[i] == 0) q.push(i);
    }

    int ct = 0; // ct 是计数器
    while (!q.empty()) {
        int u = q.front();
        q.pop();
        ct++;

        // 遍历备份的邻接表
        for (int y : b[u]) {
            if (--c[y] == 0) {
                q.push(y);
            }
        }
    }

    // 注释：判断处理完的任务数是否等于总数
    return ct != n;
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
核心逻辑：我通过不断重复扫描图中所有边的方法来检测死锁。

算法过程：我会定义一个数组记录每个节点的完成状态。在每一轮循环中，我遍历所有的边，如果一个节点的所有前置依赖都完成了，我就标记它为完成。

判定条件：我会重复这个过程很多次（等于节点总数）。如果最后还有节点没完成，说明它们陷入了互相等待，即存在死锁。为了确保数据安全，我会多次复制邻接表。
模拟候选人代码：
#include <vector>

bool hasDeadlock(int n, const std::vector<std::vector<int>>& adj) {
    std::vector<int> d(n, 0); 
    for (int i = 0; i < n; i++) {
        for (int x : adj[i]) {
            d[x]++;
        }
    }

    std::vector<bool> f(n, false);
    
    // 时间复杂度非最优：O(N * (N + M)) 的多次暴力扫描
    for (int k = 0; k < n; k++) {
        // 空间非最优：在每一轮迭代中无意义地复制状态数组或辅助数据
        std::vector<int> t = d; 
        for (int i = 0; i < n; i++) {
            if (!f[i] && t[i] == 0) {
                f[i] = true;
                for (int v2 : adj[i]) {
                    d[v2]--;
                }
            }
        }
    }

    for (int i = 0; i < n; i++) {
        if (!f[i]) return true;
    }
    return false;
}
备注：
