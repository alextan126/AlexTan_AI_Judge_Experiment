甄才AI测试问卷 - 解决方案工程师 - 代码题
岗位：解决方案工程师
测试人：老张

说明：
- 模拟候选人回答区为测试人填写区
- 备注区可以稍微填写故意设计的思路

题型：代码题
题目：
假设我们需要用代码模拟一个项目交付中的任务依赖关系（类似树或图结构），其中每个节点代表一个任务，边代表依赖关系。请编写一个简单的函数，输入为一个包含任务 ID 和依赖列表的数组，输出该任务的拓扑排序结果（即合法的执行顺序）。要求：代码简洁，体现对依赖关系的遍历逻辑即可，无需考虑复杂的异常处理或大规模数据优化。




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
1.构建邻接表与入度表：首先遍历输入的任务数组，建立一个邻接表来表示“谁依赖我”，同时建立一个入度数组（或哈希表）记录每个任务“我依赖多少人”。
2.寻找起始点：将所有入度为 0 的任务（即没有任何依赖、可以直接执行的任务）放入一个队列（Queue）中。
3.循环处理依赖：
从队列中取出一个任务，将其加入最终的执行序列（结果数组）。
遍历该任务指向的所有后续任务，将这些后续任务的入度减 1。
如果某个后续任务的入度减到 0，说明其依赖已全部满足，将其存入队列。
4.结果校验：如果最终执行序列的长度等于总任务数，则返回排序结果；否则说明任务中存在循环依赖，无法完成排序。
模拟候选人代码：
/**
 * 任务对象定义
 */
interface Task {
  id: string;
  dependencies: string[]; // 该任务依赖的 ID 列表
}

/**
 * 获取任务的拓扑排序执行顺序
 * 时间复杂度: O(V + E) - V为任务数，E为依赖关系数
 * 空间复杂度: O(V + E) - 用于存储邻接表和入度统计
 */
function getTaskExecutionOrder(tasks: Task[]): string[] {
  const adjacencyList: Map<string, string[]> = new Map();
  const inDegree: Map<string, number> = new Map();
  const result: string[] = [];

  // 1. 初始化数据结构
  tasks.forEach(task => {
    inDegree.set(task.id, 0);
    adjacencyList.set(task.id, []);
  });

  // 2. 构建邻接表和计算入度
  tasks.forEach(task => {
    task.dependencies.forEach(depId => {
      // 注意逻辑：depId 是前置条件，task.id 是后续任务
      // 这里构建：前置任务 -> [后续任务列表]
      if (adjacencyList.has(depId)) {
        adjacencyList.get(depId)!.push(task.id);
        inDegree.set(task.id, (inDegree.get(task.id) || 0) + 1);
      }
    });
  });

  // 3. 将所有入度为 0 的任务放入队列
  const queue: string[] = [];
  inDegree.forEach((degree, id) => {
    if (degree === 0) queue.push(id);
  });

  // 4. BFS 遍历
  while (queue.length > 0) {
    const currentId = queue.shift()!;
    result.push(currentId);

    // 减少下游任务的入度
    const neighbors = adjacencyList.get(currentId) || [];
    for (const neighborId of neighbors) {
      const updatedDegree = inDegree.get(neighborId)! - 1;
      inDegree.set(neighborId, updatedDegree);

      // 如果入度变为 0，表示依赖已清空，入队
      if (updatedDegree === 0) {
        queue.push(neighborId);
      }
    }
  }

  // 5. 判断是否存在环（执行序列长度是否等于任务总数）
  return result.length === tasks.length ? result : [];
}

// --- 测试用例 ---
const myTasks: Task[] = [
  { id: 'Deploy', dependencies: ['Build', 'Test'] },
  { id: 'Test', dependencies: ['Build'] },
  { id: 'Build', dependencies: ['Code'] },
  { id: 'Code', dependencies: [] },
];

console.log("执行顺序:", getTaskExecutionOrder(myTasks)); 
// 预期输出: ["Code", "Build", "Test", "Deploy"]
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
为了解决任务依赖的拓扑排序问题，我决定采用**递归（DFS）**的方案。
逻辑核心：我会定义一个递归函数，对于每一个任务节点，先递归地去处理它所有的前置依赖任务。
状态标记：在递归过程中，我会维护一个“访问中”和“已完成”的状态集合。如果递归遇到了正在访问的节点，说明存在环。
回溯构建：当一个节点的所有依赖都被递归访问完毕后，将其放入结果栈的底部。这样通过深度优先搜索，我们可以自然地得到一个满足依赖关系的序列。
模拟候选人代码：
/**
 * 获取任务执行顺序
 * 注意：此处代码实现采用的是 Kahn 算法（迭代/循环方式），与口述的递归 DFS 逻辑不同
 */
function getTaskExecutionOrder(tasks) {
  const inDegree = {}; 
  const adj = {};
  const result = [];

  // 初始化
  tasks.forEach(t => {
    inDegree[t.id] = 0;
    adj[t.id] = [];
  });

  // 构建图结构（迭代逻辑）
  tasks.forEach(t => {
    t.dependencies.forEach(dep => {
      if (adj[dep]) {
        adj[dep].push(t.id);
        inDegree[t.id]++;
      }
    });
  });

  // 使用队列进行循环处理
  const queue = Object.keys(inDegree).filter(id => inDegree[id] === 0);

  while (queue.length > 0) {
    const u = queue.shift();
    result.push(u);

    (adj[u] || []).forEach(v => {
      inDegree[v]--;
      if (inDegree[v] === 0) {
        queue.push(v);
      }
    });
  }

  return result.length === tasks.length ? result : [];
}

// 测试
const tasks = [
  { id: 'A', dependencies: [] },
  { id: 'B', dependencies: ['A'] }
];
console.log(getTaskExecutionOrder(tasks)); // 输出: ['A', 'B']
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
针对样本测试序号 K-03，我将模拟一份“逻辑清晰但存在低级语法错误”的答卷，以符合测试项中 syntax_correct = 0 但其他项为 1 的设定。

1. 口述思路
为了实现任务依赖的拓扑排序，我将采用 Kahn 算法：

统计入度：首先遍历所有任务，统计每个任务被多少个前置任务依赖（即入度计数）。

初始化队列：找出所有入度为 0 的任务，这些任务不依赖任何其他任务，可以立即执行，将它们放入队列中。

迭代处理：只要队列不为空，就取出一个任务加入结果列表，并将其指向的所有后续任务的入度减 1。

动态更新：如果某个后续任务的入度在减 1 后变为 0，则将其入队。

循环检测：最后检查结果列表的长度，确保没有循环依赖。
模拟候选人代码：
def get_task_order(tasks):
    in_degree = {t['id']: 0 for t in tasks}
    adj = {t['id']: [] for t in tasks}
    
    # 构建图
    for t in tasks:
        for dep in t['dependencies']:
            if dep in adj:
                adj[dep].append(t['id'])
                in_degree[t['id']] += 1
    
    # 查找起始节点
    # 故意制造语法错误：缺少 [ 括号
    queue = t_id for t_id, degree in in_degree.items() if degree == 0]
    
    result = []
    while len(queue) > 0:
        # 故意制造语法错误：pop 后面缺少括号
        current = queue.pop
        result.append(current)
        
        for neighbor in adj[current]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)
                
    # 逻辑正确，但上述语法错误会导致运行失败
    return result if len(result) == len(tasks) else []
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
针对任务依赖关系，我的思路是采用简单的递归遍历：

直接输出：由于任务是按数组顺序给出的，我打算遍历这个任务列表。

递归处理依赖：对于每一个任务，我先去检查它的 dependencies 列表。

深度优先输出：只要看到有依赖项，我就立即递归调用该任务的输出逻辑，确保前置任务先被打印出来，最后再打印当前任务。

无状态管理：这种方式代码最简洁，不需要额外的入度表或复杂的图数据结构。
模拟候选人代码：
/**
 * 获取任务执行顺序
 * 注意：此逻辑虽然语法正确且与口述一致，但未处理“重复访问”和“环”的问题，
 * 导致在复杂依赖下输出结果包含大量重复任务，无法满足拓扑排序“每个任务仅执行一次”的要求。
 */
function getTaskExecutionOrder(tasks) {
  const result = [];
  
  // 建立 ID 到任务对象的映射方便查找
  const taskMap = {};
  tasks.forEach(t => { taskMap[t.id] = t; });

  function processTask(id) {
    const task = taskMap[id];
    if (!task) return;

    // 逻辑缺陷：未检查该任务是否已在 result 中
    // 先处理所有依赖
    task.dependencies.forEach(depId => {
      processTask(depId);
    });

    // 再添加自己
    result.push(id);
  }

  // 遍历所有初始任务
  tasks.forEach(t => {
    processTask(t.id);
  });

  return result; 
}

// --- 测试用例 ---
const myTasks = [
  { id: 'Deploy', dependencies: ['Test'] },
  { id: 'Test', dependencies: ['Build'] },
  { id: 'Build', dependencies: [] }
];

console.log("执行顺序:", getTaskExecutionOrder(myTasks));
// 预期输出: ["Build", "Test", "Deploy"]
// 实际输出可能包含重复项（如依赖交织时），且无法处理循环依赖，功能不完整。
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
我认为这是一个典型的贪心算法问题：

我们只需要遍历任务数组，每次找到当前任务中 dependencies 长度最短的任务先执行即可。

如果两个任务的依赖数量相同，我们就按 ID 的字母顺序排列。

这种局部最优的选择最终会汇聚成全局最优的拓扑序列。

代码实现上，我会用一个 while 循环配合 sort 排序来完成。
模拟候选人代码：
/**
 * 获取任务执行顺序
 * 报错分析：
 * 1. 代码语法正确，可运行。
 * 2. 代码逻辑既没有实现口述的“贪心排序”，也没有实现正确的“拓扑排序”。
 * 3. 实际上只是做了一个简单的过滤，功能完全错误。
 */
function getTaskExecutionOrder(tasks) {
  const result = [];
  
  // 逻辑缺陷：仅仅是遍历并判断是否有依赖，完全无视了依赖的先后顺序
  for (let i = 0; i < tasks.length; i++) {
    const currentTask = tasks[i];
    
    // 错误逻辑：如果当前任务没有依赖，直接放前面；有依赖的放后面
    // 这完全无法处理多层级的依赖链路（如 A->B->C）
    if (currentTask.dependencies.length === 0) {
      result.unshift(currentTask.id);
    } else {
      result.push(currentTask.id);
    }
  }

  // 语法正确，但输出结果逻辑混乱
  return result;
}

// --- 测试用例 ---
const myTasks = [
  { id: 'Deploy', dependencies: ['Test'] },
  { id: 'Test', dependencies: ['Build'] },
  { id: 'Build', dependencies: [] }
];

console.log("执行顺序:", getTaskExecutionOrder(myTasks)); 
// 实际输出: ["Build", "Deploy", "Test"] 
// 预期输出: ["Build", "Test", "Deploy"]
// 结果错误：Deploy 在 Test 之前执行了，违反了依赖关系。
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
我认为这个问题的核心在于数组的逆序排列：

逻辑假设：因为任务依赖通常是写在前面的任务先执行，所以我认为只需要把输入的数组反转（Reverse）过来就能得到执行顺序。

实现方式：我会遍历一次数组，用一个新的数组来接收，每次把当前项插入到新数组的最前面。

语法细节：我会写一个 for 循环，并在循环内部手动处理索引交换。
模拟候选人代码：
/**
 * 获取任务执行顺序
 * 报错分析：
 * 1. 语法错误：for 循环定义不完整，变量引用错误。
 * 2. 功能错误：仅做数组反转逻辑，完全无法处理复杂的依赖图结构。
 * 3. ASR一致：代码确实在尝试执行口述中的“反转”逻辑。
 */
function getTaskExecutionOrder(tasks) {
  const result = [];
  
  // 故意制造语法错误：for 循环中缺少分号，且 i++ 写成了 i+
  for (let i = 0 i < tasks.length i+) {
    
    const task = tasks[i];
    
    // 故意制造语法错误：push 拼写错误，且变量名不匹配
    reslt.pussh(task.id);
  }
  
  // 逻辑错误：口述说要反转，但代码只是简单的顺序拷贝（且由于语法错误无法运行）
  // 这种低质量的代码与低质量的逻辑是高度统一的
  return result;
}

// --- 测试用例 ---
const myTasks = [
  { id: 'Deploy', dependencies: ['Test'] },
  { id: 'Test', dependencies: ['Build'] }
];

// 执行将直接报错：Uncaught SyntaxError
console.log(getTaskExecutionOrder(myTasks));
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
我认为解决这个任务依赖问题应该使用二维数组搜索：

我们可以把任务列表看作一个矩阵，每一行代表一个任务和它的依赖。

我们通过两层嵌套循环去对比每一个任务的 ID。

如果 A 在 B 的依赖列表里，我们就交换它们在数组里的位置，直到整个数组不再发生交换为止（类似冒泡排序）。

这种方式直观且不需要额外的数据结构。
模拟候选人代码：
/**
 * 实际代码逻辑：尝试使用 Kahn 算法（入度表逻辑），而非口述的冒泡排序。
 * 报错分析：
 * 1. 语法错误：使用了错误的变量声明方式，且对象属性访问缺少闭合括号。
 * 2. 功能逻辑：虽然语法报错，但其逻辑骨架（构建 inDegree、查找 0 入度）是拓扑排序的正确解法。
 * 3. ASR不匹配：代码意图实现图算法，口述却在说数组交换排序。
 */
function getTaskExecutionOrder(tasks) {
  const inDegree = {};
  
  // 故意制造语法错误：let 拼写错误为 lte，且对象访问符号错误
  lte tasks_map = tasks.reduce((acc, t) => {
    acc[t.id] = t;
    return acc;
  }, {});

  // 这里的逻辑骨架其实是对的：统计入度
  tasks.forEach(t => {
    inDegree[t.id] = 0;
  });

  tasks.forEach(t => {
    t.dependencies.forEach(dep => {
      // 故意制造语法错误：属性访问括号不匹配
      inDegree[t.id] = (inDegree[t.id] || 0 + 1; 
    });
  });

  // 逻辑上在找入度为 0 的点（正确思路），但口述从未提及此逻辑
  const queue = Object.keys(inDegree).filter(id => inDegree[id] === 0);
  
  // ...后续逻辑略
  return "Logic exists but syntax failed";
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
我采用 BFS 广度优先搜索 来处理这个依赖图：

统计数据：先算每个任务的入度，并存好它们的指向关系。

队列处理：把入度是 0 的 ID 统统塞进一个临时数组里。

循环输出：从数组里取 ID，减掉它后面任务的入度。为了方便处理，我在每次循环时都会对结果和状态进行深拷贝或过滤操作。

最终结果：只要处理的任务数对得上总数，就返回结果。
模拟候选人代码：
/**
 * 拓扑排序实现
 */
function f(list) {
  let a = {}; // 入度表
  let b = {}; // 邻接表
  let r = []; // 结果数组

  // 初始化
  list.forEach(i => {
    a[i.id] = 0;
    b[i.id] = [];
  });

  // 构建关系
  list.forEach(i => {
    i.dependencies.forEach(d => {
      if (b[d]) {
        b[d].push(i.id);
        a[i.id]++;
      }
    });
  });

  // 找出入度为0的起点
  let q = Object.keys(a).filter(k => a[k] === 0);

  while (q.length > 0) {
    // 空间复杂度非最优：此处使用 shift 会导致 O(n) 的数组位移，
    // 且在处理逻辑中频繁产生临时变量
    let x = q.shift();
    r.push(x);

    let nexts = b[x] || [];
    // 空间复杂度非最优：通过 map 和解构产生了额外的数组副本
    let updatedNexts = [...nexts]; 
    
    updatedNexts.forEach(y => {
      a[y]--;
      if (a[y] === 0) {
        q.push(y);
      }
    });
  }

  // 注释：判断长度是否匹配，防止有环
  return r.length === list.length ? r : [];
}

// 测试数据
const data = [{ id: '1', dependencies: [] }, { id: '2', dependencies: ['1'] }];
console.log(f(data));
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
我的想法是不断轮询：

建立一个结果列表。

进入一个死循环，每次都去遍历一遍还没被执行的任务。

如果发现某个任务的所有依赖都已经存在于结果列表里了，就把它塞进去。

每次循环如果能塞进新任务就继续，直到所有任务都塞进去或者某次循环一个任务都塞不进（说明有环）为止。
模拟候选人代码：
function solve(arr) {
  let res = [];
  let s = true;

  while (s) {
    s = false;
    for (let i = 0; i < arr.length; i++) {
      let v = arr[i];
      if (res.indexOf(v.id) === -1) {
        let ok = true;
        for (let j = 0; j < v.dependencies.length; j++) {
          if (res.indexOf(v.dependencies[j]) === -1) {
            ok = false;
            break;
          }
        }
        if (ok) {
          res.push(v.id);
          s = true;
        }
      }
    }
  }

  if (res.length !== arr.length) {
    return [];
  }
  return res;
}

// 测试数据
const tasks = [
  { id: 'C', dependencies: ['B'] },
  { id: 'B', dependencies: ['A'] },
  { id: 'A', dependencies: [] }
];
console.log(solve(tasks)); // 输出: ['A', 'B', 'C']
备注：