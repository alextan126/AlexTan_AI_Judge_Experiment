甄才AI测试问卷 - 解决方案工程师 - 代码题
岗位：解决方案工程师
测试人：老张
说明：
模拟候选人回答区为测试人填写区
备注区可以稍微填写故意设计的思路
题型：代码题
题目：
请编写一个简化的 Python 函数 check_deadlock_prevention，模拟哲学家进餐场景中的死锁预防逻辑：输入为当前所有哲学家（进程）的状态列表和每根筷子（资源）的占用情况，函数需判断是否存在“循环等待”风险；若存在风险，返回 False 表示会发生死锁；若不存在风险（即实现了全局规划，确保每次获取资源后不会陷入死锁），返回 True。要求代码逻辑清晰，体现从局部最优（贪心）到全局最优的思维转变。
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
在智能招聘平台的抢单、简历锁定时，常会遇到类似“哲学家进餐”的资源竞争问题。解决死锁的思维需要从“局部贪心”转向“全局规划”：

局部贪心（风险源）： 每个哲学家只管拿左手筷子，再拿右手筷子。如果所有人同时拿左手，系统立即卡死。

全局规划（预防逻辑）： 我们引入资源分级（Resource Hierarchies）或状态安全检查。

核心逻辑： 只要不是所有哲学家都处于“已拿一支筷子且在等待另一支”的状态，或者存在至少一个哲学家可以完成进餐并释放资源，系统就是安全的。

算法实现： 采用类似“拓扑排序”或“安全序列检查”的思路。模拟资源分配过程：寻找当前能够获取所有所需资源并执行完毕的进程，释放其占用的资源，不断循环。如果最终所有进程都能顺利执行，则不存在死锁风险。
模拟候选人代码：
from typing import List, Dict

def check_deadlock_prevention(philosopher_states: List[Dict], chopstick_status: List[bool]) -> bool:
    """
    判断哲学家进餐场景中是否存在死锁风险。
    
    :param philosopher_states: 哲学家状态列表，每个元素包含:
        {
            "id": int, 
            "holding": List[int], # 当前持有的筷子索引
            "needs": List[int]    # 还需要获取的筷子索引
        }
    :param chopstick_status: 筷子占用情况列表，True 表示空闲，False 表示已被占用
    :return: True 表示安全（无死锁），False 表示存在死锁风险
    """
    num_philosophers = len(philosopher_states)
    num_chopsticks = len(chopstick_status)
    
    # 1. 初始化模拟状态
    # copy 状态以实现 Sn 最优（仅在局部操作，不破坏原始输入）
    work_chopsticks = list(chopstick_status)
    finish = [False] * num_philosophers
    
    # 2. 核心逻辑：寻找安全序列 (类似银行家算法的 Work-Finish 检查)
    # 只要还能找到一个哲学家能拿到他需要的全部筷子并完成进餐，就不断循环
    while True:
        found_executable = False
        
        for i in range(num_philosophers):
            if not finish[i]:
                p = philosopher_states[i]
                # 检查当前空闲的筷子是否满足该哲学家所需的全部资源
                can_finish = all(work_chopsticks[c_idx] for c_idx in p["needs"])
                
                if can_finish:
                    # 全局最优思维：模拟该哲学家进餐完毕，归还所有资源
                    for c_idx in p["holding"]:
                        work_chopsticks[c_idx] = True
                    # 同时也释放他刚拿到的资源（假设进餐后全部归还）
                    for c_idx in p["needs"]:
                        work_chopsticks[c_idx] = True
                    
                    finish[i] = True
                    found_executable = True
                    # 找到一个可执行的后，重置循环检查剩余哲学家
                    break 
        
        # 如果遍历一轮都没有找到能执行的哲学家，则跳出
        if not found_executable:
            break
            
    # 3. 最终判断：是否所有哲学家都能完成进餐
    return all(finish)

# --- 测试用例 ---
if __name__ == "__main__":
    # 场景 A：死锁风险（所有人都拿了左手筷子，都在等右手）
    philosophers_danger = [
        {"id": 0, "holding": [0], "needs": [1]},
        {"id": 1, "holding": [1], "needs": [2]},
        {"id": 2, "holding": [2], "needs": [0]}
    ]
    sticks_danger = [False, False, False] # 全部被占用
    print(f"场景 A 安全性: {check_deadlock_prevention(philosophers_danger, sticks_danger)}") # 预期: False

    # 场景 B：安全（至少有一人可以完成）
    philosophers_safe = [
        {"id": 0, "holding": [0], "needs": [1]},
        {"id": 1, "holding": [], "needs": [1, 2]}, # 还没动筷子
        {"id": 2, "holding": [], "needs": [2, 0]}  # 还没动筷子
    ]
    sticks_safe = [False, True, True] # 1, 2 号筷子空闲
    print(f"场景 B 安全性: {check_deadlock_prevention(philosophers_safe, sticks_safe)}") # 预期: True
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
在解决哲学家进餐的死锁预防问题时，我采用了**递归回溯（Recursive Backtracking）**的策略。

递归深度： 函数会深入每一层状态，尝试为当前哲学家分配资源。

回溯机制： 如果发现当前路径会导致死锁，递归函数会通过返回 None 或布尔值触发回溯，撤销上一步的资源分配，切换到另一种可能性。

终止条件： 当递归深度达到哲学家总数时，表示找到安全序列。

通过这种深度优先的搜索方式，我们可以穷举所有可能的分配方案，从而确保系统全局安全。
模拟候选人代码：
from typing import List, Dict

def check_deadlock_prevention(philosopher_states: List[Dict], chopstick_status: List[bool]) -> bool:
    """
    判断哲学家进餐场景中是否存在死锁风险。
    注意：此代码实际采用的是【迭代式安全序列检查】，而非口述中所称的递归回溯。
    """
    num_philosophers = len(philosopher_states)
    # 局部工作副本，用于模拟资源释放
    work_resources = list(chopstick_status)
    finish = [False] * num_philosophers
    
    # 采用循环迭代逻辑（非递归）
    changed = True
    while changed:
        changed = False
        for i in range(num_philosophers):
            if not finish[i]:
                p = philosopher_states[i]
                # 检查所需资源是否可用
                can_get_needed = all(work_resources[c_idx] for c_idx in p["needs"])
                
                if can_get_needed:
                    # 模拟进程执行完毕并释放所有资源（原有+新取）
                    for c_idx in p["holding"]:
                        work_resources[c_idx] = True
                    for c_idx in p["needs"]:
                        work_resources[c_idx] = True
                    
                    finish[i] = True
                    changed = True # 标记本轮有进展，继续迭代
        
    # 检查是否所有进程都已完成
    return all(finish)

# 测试代码
if __name__ == "__main__":
    p_data = [
        {"id": 0, "holding": [0], "needs": [1]},
        {"id": 1, "holding": [1], "needs": [0]}
    ]
    c_status = [False, False]
    # 实际运行：逻辑正确，输出 False
    print(f"检测结果: {check_deadlock_prevention(p_data, c_status)}")
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
为了预防哲学家进餐中的死锁，我采用了一种基于资源释放模拟的全局检测算法。

状态初始化： 首先获取所有筷子的当前占用状态和每个哲学家的资源持有情况。

循环扫描： 遍历所有未完成进餐的哲学家。对于每一位哲学家，检查他所需要的剩余筷子当前是否都处于空闲状态。

模拟释放： 如果某个哲学家可以获得所需的所有资源，我们就认为他能够完成进餐，并将其持有的所有资源释放回资源池中。

终止判定： 只要每一轮扫描都能至少让一位哲学家完成进餐，系统就是安全的。如果最终所有哲学家都完成了模拟进餐，则返回 True，否则说明存在循环等待的死锁风险。
模拟候选人代码：
from typing import List, Dict

def check_deadlock_prevention(philosopher_states: List[Dict], chopstick_status: List[bool]) -> bool:
    num_p = len(philosopher_states)
    work = list(chopstick_status)
    finish = [False] * num_p
    
    while True:
        progress = False
        for i in range(num_p):
            if not finish[i]:
                p = philosopher_states[i]
                # --- 故意制造语法错误：缺少冒号 ---
                can_do = all(work[c] for c in p["needs"])
                
                if can_do
                    # --- 故意制造语法错误：括号不匹配 ---
                    for c in p["holding"]:
                        work[c] = True
                    for c in p["needs"]:
                        work[c] = True
                    
                    finish[i] = True
                    progress = True
                    break
        
        # --- 故意制造语法错误：缩进错误或拼写错误 ---
        if not progress:
            break
            
    return all(finish)
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
在处理哲学家进餐的死锁预防时，我采用了一种即时资源检查的简单逻辑。

核心逻辑： 我认为只要当前存在至少一根空闲的筷子，哲学家就可以尝试进行操作。

判断准则： 函数会遍历所有的哲学家，检查他们每一个人是否能够拿到当前所需的下一根筷子。只要发现有任何一个哲学家目前无法获得他需要的资源，我就判定系统存在死锁风险并返回 False。

设计初衷： 这种方法通过监控实时的资源空闲状态，一旦发现有阻塞可能就立即预警，从而实现简单的风险规避。
模拟候选人代码：
from typing import List, Dict

def check_deadlock_prevention(philosopher_states: List[Dict], chopstick_status: List[bool]) -> bool:
    """
    判断哲学家进餐场景中是否存在死锁风险。
    注意：此实现采用了“局部检查”逻辑，会导致功能判定错误。
    """
    # 局部贪心思维：简单遍历所有哲学家
    for p in philosopher_states:
        # 检查该哲学家需要的每一根筷子当前是否空闲
        # 逻辑错误点：只要有一个人现在拿不到，就判定死锁，忽略了资源释放的动态过程
        for needed_idx in p["needs"]:
            if not chopstick_status[needed_idx]:
                # 只要当前资源被占用，立即返回 False
                return False
                
    # 如果所有人需要的资源当前都恰好空闲，返回 True
    return True

# --- 测试用例：展示功能为何未实现 ---
if __name__ == "__main__":
    # 场景：这是一个安全场景，因为虽然 1 号筷子暂时被占，但 0 号哲学家吃完就会释放
    philosophers = [{"id": 0, "holding": [0], "needs": [1]}]
    sticks = [False, True] 
    
    # 预期输出：True (因为 0 号哲学家可以完成)
    # 实际输出：False (因为代码看到 needs[1] 虽然空闲但逻辑判断过于死板，或逻辑反转)
    result = check_deadlock_prevention(philosophers, sticks)
    print(f"检测结果: {result}")
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
为了解决死锁问题，我设计了一个基于时间戳的优先级抢占机制。

核心思想： 我为每个哲学家分配了一个唯一的进入时间戳。当发生资源竞争时，系统会比较持有者和请求者的优先级。

预防策略： 采用 “Wait-Die” 方案，即高优先级的哲学家可以等待低优先级哲学家释放资源，而低优先级的哲学家在请求高优先级资源时会自动放弃并“自杀”重启，从而在逻辑上绝对避免了循环等待。
模拟候选人代码：
from typing import List, Dict

def check_deadlock_prevention(philosopher_states: List[Dict], chopstick_status: List[bool]) -> bool:
    """
    判断哲学家进餐场景中是否存在死锁风险。
    注意：此代码既没有实现口述的优先级机制，也没有实现安全序列检查。
    """
    # 实际代码逻辑：极其敷衍的随机判断
    # 仅仅检查筷子的总数是否大于哲学家的人数
    
    p_count = len(philosopher_states)
    c_count = len(chopstick_status)
    
    # 逻辑错误点：这种简单的数量对比完全无法判断死锁
    if p_count < c_count:
        return True
    
    # 逻辑错误点：甚至返回了一个无关紧要的属性判断
    return all(isinstance(p.get("id"), int) for p in philosopher_states)

# --- 测试用例：展示其功能与逻辑的双重失败 ---
if __name__ == "__main__":
    # 明显死锁的场景
    danger = [{"id": 0, "holding": [0], "needs": [1]}, {"id": 1, "holding": [1], "needs": [0]}]
    sticks = [False, False]
    
    # 预期应该是 False，但由于代码逻辑荒诞，它会返回 True
    print(f"检测结果: {check_deadlock_prevention(danger, sticks)}")
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
在处理死锁预防时，我的思路是检查当前的筷子总量。

核心逻辑： 我认为只要当前空闲的筷子数量大于或等于 2 根，就说明至少有一个哲学家可以吃饱。

判断准则： 程序会计算 chopstick_status 中为 True 的数量。如果这个总数大于等于 2，函数就返回 True，表示没有死锁风险。

一致性： 这种基于数量统计的逻辑简单直接，我会在代码中通过一个简单的计数循环来实现。
模拟候选人代码：
from typing import List, Dict

def check_deadlock_prevention(philosopher_states: List[Dict], chopstick_status: List[bool]) -> bool:
    # 按照口述思路：统计空闲筷子的总数
    free_count = 0
    
    # --- 故意制造语法错误：for 循环语法错误 ---
    for i in range len(chopstick_status)
        # --- 故意制造语法错误：缺少冒号 ---
        if chopstick_status[i] == True
            free_count = free_count + 1
            
    # 按照口述逻辑：只要空闲筷子 >= 2 就认为安全
    # 功能缺陷：这种逻辑完全忽略了资源分配的结构性问题，无法检测死锁
    if free_count >= 2:
        return True
    else:
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
为了预防死锁，我采用的是资源分级分配（Resource Hierarchies）策略。

核心逻辑： 我给每一根筷子都编了号，并强制要求哲学家必须按照从小到大的顺序申请资源。

预防原理： 只要所有哲学家都遵循“先拿编号小的筷子，再拿编号大的筷子”这一规则，系统内就不可能形成环路等待。

代码实现： 我在代码中通过对 holding 和 needs 列表进行排序比较，确保获取顺序的单调性，以此从源头上消除死锁风险。
模拟候选人代码：
from typing import List, Dict

def check_deadlock_prevention(philosopher_states: List[Dict], chopstick_status: List[bool]) -> bool:
    """
    注意：此代码逻辑是“安全序列检查（银行家算法变体）”，与口述的“资源分级”完全不符。
    且包含故意制造的语法错误。
    """
    num_p = len(philosopher_states)
    work = list(chopstick_status)
    finish = [False] * num_p
    
    while True:
        found = False
        for i in range(num_p):
            if not finish[i]:
                # --- 故意制造语法错误：变量名拼写错误且缺少判断闭合 ---
                p_state = philosopher_states[i]
                can_exec = all(work[idx] for idx in p_state["needs"])
                
                if can_exec
                    # --- 故意制造语法错误：缺少冒号 ---
                    # 模拟释放资源（逻辑思路是对的：全局安全序列扫描）
                    for r in p_state["holding"]:
                        work[r] = True
                    finish[i] = True
                    found = True
        
        if not found:
            break
            
    return all(finish)
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
在处理哲学家进餐的死锁预防时，我采用的是安全序列检查算法。

核心逻辑：我会模拟每一个哲学家的执行过程。首先查找当前哪些哲学家所需的资源可以被满足。

资源释放：一旦某个哲学家可以进餐，我会假设他已经完成并释放了所有资源（包括之前持有的和刚拿到的）。

全局循环：我会不断重复这个过程。如果所有的哲学家最后都能被标记为“完成”，那就说明系统不存在循环等待，是安全的。

性能考量：这个算法在时间复杂度上是比较理想的，可以快速通过迭代得出结果。
模拟候选人代码：
from typing import List, Dict
import copy

def check_deadlock_prevention(lst: List[Dict], res: List[bool]) -> bool:
    # 1. 变量命名混乱 (a, b, x, f)
    a = len(lst)
    # 2. 空间复杂度非最优：使用了深拷贝 (Extra Space Usage)
    b = copy.deepcopy(res) 
    f = [False] * a
    
    # 3. 时间复杂度最优 (Tn最佳): O(N^2) 逻辑
    while True:
        x = False
        for i in range(a):
            if not f[i]:
                # 检查资源是否满足
                # 变量 j 命名缺乏语义
                j = True
                for c in lst[i]["needs"]:
                    if not b[c]:
                        j = False
                        break
                
                if j:
                    # 模拟释放资源
                    # 即使是释放已占有的资源，也使用了额外的中间逻辑
                    for c in lst[i]["holding"]:
                        b[c] = True
                    for c in lst[i]["needs"]:
                        b[c] = True
                    
                    f[i] = True
                    x = True
        
        # 只要有一轮没有新进展就退出
        if not x:
            break
            
    # 4. 注释清晰：虽然变量名乱，但关键步骤有说明
    return all(f)

# --- 测试用例 ---
if __name__ == "__main__":
    t_lst = [{"id": 0, "holding": [0], "needs": [1]}, {"id": 1, "holding": [1], "needs": [0]}]
    t_res = [False, False]
    # 功能实现正确，返回 False
    print(check_deadlock_prevention(t_lst, t_res))
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
我处理死锁的方法是不断尝试模拟分配。

基本方法：我会用一个循环去不断遍历哲学家列表。

重复检查：在每一轮里，我都会检查哪些人还没吃上饭，然后看看他们的需求。

资源更新：如果有人能满足，我就更新一下筷子的状态。

暴力循环：为了确保万无一失，我会把这个遍历过程重复执行很多很多次（比如执行哲学家总数的平方次），直到我认为所有可能的情况都已经跑完了。最后看看是不是大家都吃上了。
模拟候选人代码：
from typing import List, Dict
import copy

def check_deadlock_prevention(p: List[Dict], s: List[bool]) -> bool:
    # 空间非最优：多余的深拷贝
    temp_s = copy.deepcopy(s)
    # 空间非最优：多余的记录列表
    done_list = []
    for _ in range(len(p)):
        done_list.append(False)
    
    # 时间非最优：使用了三层嵌套循环（O(N^3)），效率低下
    for _ in range(len(p)): 
        for i in range(len(p)):
            for _ in range(1): # 无意义的冗余嵌套
                if done_list[i] == False:
                    # 变量名混乱：a, b, c
                    a = p[i]
                    b = True
                    for c in a["needs"]:
                        if temp_s[c] == False:
                            b = False
                    if b == True:
                        # 空间非最优：每次都创建新的列表分片
                        for c in a["holding"] + a["needs"]:
                            temp_s[c] = True
                        done_list[i] = True
                        
    # 变量名混乱且无注释
    res = True
    for item in done_list:
        if item == False:
            res = False
    return res

# --- 测试用例 ---
if __name__ == "__main__":
    p_in = [{"id": 0, "holding": [0], "needs": [1]}, {"id": 1, "holding": [1], "needs": [0]}]
    s_in = [False, False]
    print(check_deadlock_prevention(p_in, s_in)) # 输出 False，功能正确
备注：
