解决方案工程师第一轮测试样本（Item 1）：
- 描述：三种题型都是全对样本 A-01 / C-01 / K-01
- 测试轮数： 5轮
- Ground Truth:
        concept: passed=True  决定项=[1]  加分项=[1, 1, 1, 1, 1, 1]
        application: passed=True  决定项=[1]  加分项=[1, 1]
        code: passed=True  决定项=[1, 1, 1]  加分项=[1, 1, 1, 1]

- Testing Record:

| 轮次 | concept dp | concept ep | application dp | application ep | code dp | code ep |
|------|-----------|-----------|---------------|---------------|---------|---------|
| R01  | [1]       | [1,1,1,1,1,1] | [1]           | [1,1]         | [1,1,1] | [1,1,1,1] |
| R02  | [1]       | [1,1,1,1,1,1] | [1]           | [1,1]         | [1,1,1] | [1,1,1,1] |
| R03  | [1]       | [1,1,1,1,1,1] | [1]           | [1,1]         | [1,1,1] | [1,1,1,1] |
| R04  | [1]       | [1,1,1,1,1,1] | [1]           | [1,1]         | [1,1,1] | [1,1,1,1] |
| R05  | [1]       | [1,1,1,1,1,1] | [1]           | [1,1]         | [1,1,1] | [1,1,1,1] |

dp = decision_results, ep = extra_results

- 观察: 5轮测试中所有判定点结果完全一致，与 Ground Truth 100% 匹配，无任何波动。

- Metrics:

| 指标 | 公式 | 值 |
|------|------|----|
| 整体准确率 | matched_all / total_all = 17×5 / 17×5 = 85/85 | **100.00%** |
| 决定项准确率 | matched_dec / total_dec = 5×5 / 5×5 = 25/25 | **100.00%** |
| 加分项准确率 | matched_ext / total_ext = 12×5 / 12×5 = 60/60 | **100.00%** |
| 短路合规率 | N/A (GT全Pass，无短路场景) | **100.00%** (vacuous truth) |

- 样本判定稳定性 Gini Impurity（逐点）:

| 题型 | 类别 | 判定点 | 5轮序列 | G |
|------|------|--------|---------|---|
| concept | dp | define | [1,1,1,1,1] | 0.0000 |
| concept | ep | keyword | [1,1,1,1,1] | 0.0000 |
| concept | ep | keyword_first_sentence | [1,1,1,1,1] | 0.0000 |
| concept | ep | keyword_no_repeat | [1,1,1,1,1] | 0.0000 |
| concept | ep | not_overtime | [1,1,1,1,1] | 0.0000 |
| concept | ep | define_first_sentence | [1,1,1,1,1] | 0.0000 |
| concept | ep | order_define_explain | [1,1,1,1,1] | 0.0000 |
| application | dp | correct_option | [1,1,1,1,1] | 0.0000 |
| application | ep | hook_original | [1,1,1,1,1] | 0.0000 |
| application | ep | deduction_correct | [1,1,1,1,1] | 0.0000 |
| code | dp | syntax_correct | [1,1,1,1,1] | 0.0000 |
| code | dp | function_correct | [1,1,1,1,1] | 0.0000 |
| code | dp | asr_match | [1,1,1,1,1] | 0.0000 |
| code | ep | time_optimal | [1,1,1,1,1] | 0.0000 |
| code | ep | space_optimal | [1,1,1,1,1] | 0.0000 |
| code | ep | code_readability | [1,1,1,1,1] | 0.0000 |
| code | ep | comment_readability | [1,1,1,1,1] | 0.0000 |

全部 17 个判定点 Gini = 0，完全稳定。

---

解决方案工程师第二轮测试样本（Item 2）：
- 描述：三种题型都是瑕疵样本 A-02 / C-02 / K-02
- 测试轮数： 5轮
- Ground Truth:
        concept: passed=True  决定项=[1]  加分项=[1, 0, 0, 1, 1, 1]
        application: passed=True  决定项=[1]  加分项=[1, 0]
        code: passed=False  决定项=[1, 1, 0]  加分项=[]（短路，asr_match=0）

- Testing Record:

| 轮次 | concept dp | concept ep | application dp | application ep | code dp | code ep |
|------|-----------|-----------|---------------|---------------|---------|---------|
| R01  | [1]       | [1,0,1,1,1,1] | [1]           | [1,0]         | [0,1,0] | []      |
| R02  | [1]       | [1,0,1,1,1,1] | [1]           | [1,0]         | [0,1,0] | []      |
| R03  | [1]       | [1,0,1,1,1,1] | [1]           | [1,0]         | [1,1,0] | []      |
| R04  | [1]       | [1,0,1,1,1,1] | [1]           | [1,0]         | [0,1,0] | []      |
| R05  | [1]       | [1,0,1,1,1,1] | [1]           | [1,0]         | [0,0,0] | []      |

dp = decision_results, ep = extra_results

- 观察:
  - concept dp/ep 和 application dp/ep 5轮完全一致
  - concept ep: 系统返回 [1,0,1,1,1,1]，GT 为 [1,0,0,1,1,1]，keyword_no_repeat 与 GT 不一致（系统判1，GT期望0）
  - application ep: 系统返回 [1,0]，与 GT [1,0] 完全一致
  - **code syntax_correct 出现波动**: R01/R02/R04/R05 判为0，R03 判为1，GT 期望1
  - **code function_correct 出现波动**: R01-R04 判为1（与GT一致），R05 判为0（与GT不一致）
  - code asr_match=0 5轮稳定，与 GT 一致；系统正确短路，ep 为空

- Metrics:

| 指标 | 公式 | 值 |
|------|------|----|
| 整体准确率 | (11+11+12+11+10) / (13×5) = 55/65 | **84.62%** |
| 决定项准确率 | (4+4+5+4+3) / (5×5) = 20/25 | **80.00%** |
| 加分项准确率 | 7×5 / (8×5) = 35/40 | **87.50%** |
| 短路合规率 | 5/5 (code短路正确) | **100.00%** |

计算依据:
- 每轮判定点数: 决定项 5个, 加分项 8个 (concept:6 + application:2 + code:0短路), 共 13个
- 决定项每轮匹配: R01=4/5, R02=4/5, R03=5/5, R04=4/5, R05=3/5
- 加分项每轮匹配: concept 5/6 + application 2/2 + code 0/0 = 7/8 (每轮相同)
- 决定项不匹配项: code syntax_correct(R01/R02/R04/R05: sys=0,GT=1), code function_correct(R05: sys=0,GT=1)
- 加分项不匹配项: concept keyword_no_repeat(sys=1,GT=0)

- 样本判定稳定性 Gini Impurity（逐点）:

| 题型 | 类别 | 判定点 | 5轮序列 | G |
|------|------|--------|---------|---|
| concept | dp | define | [1,1,1,1,1] | 0.0000 |
| concept | ep | keyword | [1,1,1,1,1] | 0.0000 |
| concept | ep | keyword_first_sentence | [0,0,0,0,0] | 0.0000 |
| concept | ep | keyword_no_repeat | [1,1,1,1,1] | 0.0000 |
| concept | ep | not_overtime | [1,1,1,1,1] | 0.0000 |
| concept | ep | define_first_sentence | [1,1,1,1,1] | 0.0000 |
| concept | ep | order_define_explain | [1,1,1,1,1] | 0.0000 |
| application | dp | correct_option | [1,1,1,1,1] | 0.0000 |
| application | ep | hook_original | [1,1,1,1,1] | 0.0000 |
| application | ep | deduction_correct | [0,0,0,0,0] | 0.0000 |
| code | dp | syntax_correct | [0,0,1,0,0] | **0.3200** |
| code | dp | function_correct | [1,1,1,1,0] | **0.3200** |
| code | dp | asr_match | [0,0,0,0,0] | 0.0000 |

**注意: code syntax_correct Gini = 1 - (4/5)² - (1/5)² = 1 - 0.64 - 0.04 = 0.3200，出现不稳定！**
**code function_correct Gini = 1 - (4/5)² - (1/5)² = 0.3200，R05 判定结果偏离其他轮次。**
K-02 样本的代码判定中 syntax_correct 和 function_correct 两项存在波动。

---

解决方案工程师第三轮测试样本（Item 3）：
- 描述：三种题型都是错误样本 A-04 / C-04 / K-05
- 测试轮数： 5轮
- Ground Truth:
        concept: passed=False  决定项=[0]  加分项=[]（短路）
        application: passed=False  决定项=[0]  加分项=[]（短路）
        code: passed=False  决定项=[1, 0, 0]  加分项=[]（短路）

- Testing Record:

| 轮次 | concept dp | concept ep | application dp | application ep | code dp | code ep |
|------|-----------|-----------|---------------|---------------|---------|---------|
| R01  | [0]       | []        | [0]           | []            | [1,0,0] | []      |
| R02  | [0]       | []        | [0]           | []            | [1,0,0] | []      |
| R03  | [0]       | []        | [0]           | []            | [1,0,0] | []      |
| R04  | [0]       | []        | [0]           | []            | [1,0,0] | []      |
| R05  | [0]       | []        | [0]           | []            | [1,0,0] | []      |

dp = decision_results, ep = extra_results

- 观察: 5轮测试中所有判定点结果完全一致，与 Ground Truth 100% 匹配，三种题型均正确触发短路，ep 全部为空。

- Metrics:

| 指标 | 公式 | 值 |
|------|------|----|
| 整体准确率 | matched_all / total_all = 5×5 / 5×5 = 25/25 | **100.00%** |
| 决定项准确率 | matched_dec / total_dec = 5×5 / 5×5 = 25/25 | **100.00%** |
| 加分项准确率 | N/A（三种题型均短路，无加分项可比较） | **N/A** |
| 短路合规率 | compliant / applicable = 15/15 (三种题型×5轮均正确短路) | **100.00%** |

计算依据:
- 每轮判定点数: 决定项 5个 (concept:1 + application:1 + code:3), 加分项 0个 (全部短路), 共 5个
- 5轮全部与 GT 匹配 → 25/25

- 样本判定稳定性 Gini Impurity（逐点）:

| 题型 | 类别 | 判定点 | 5轮序列 | G |
|------|------|--------|---------|---|
| concept | dp | define | [0,0,0,0,0] | 0.0000 |
| application | dp | correct_option | [0,0,0,0,0] | 0.0000 |
| code | dp | syntax_correct | [1,1,1,1,1] | 0.0000 |
| code | dp | function_correct | [0,0,0,0,0] | 0.0000 |
| code | dp | asr_match | [0,0,0,0,0] | 0.0000 |

全部 5 个判定点 Gini = 0，完全稳定。
