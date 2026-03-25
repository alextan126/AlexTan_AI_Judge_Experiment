算法工程师第一轮测试样本（Item 1）：
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

算法工程师第二轮测试样本（Item 2）：
- 描述：三种题型都是瑕疵样本 A-02 / C-02 / K-02
- 测试轮数： 5轮
- Ground Truth:
        concept: passed=True  决定项=[1]  加分项=[1, 0, 0, 1, 1, 1]
        application: passed=True  决定项=[1]  加分项=[1, 0]
        code: passed=False  决定项=[1, 1, 0]  加分项=[]（短路，asr_match=0）

- Testing Record:

| 轮次 | concept dp | concept ep | application dp | application ep | code dp | code ep |
|------|-----------|-----------|---------------|---------------|---------|---------|
| R01  | [1]       | [1,1,1,1,1,1] | [1]           | [1,1]         | [1,1,0] | []      |
| R02  | [1]       | [1,1,1,1,1,1] | [1]           | [1,1]         | [1,1,0] | []      |
| R03  | [1]       | [1,1,1,1,1,1] | [1]           | [1,1]         | [1,1,0] | []      |
| R04  | [1]       | [1,1,1,1,1,1] | [1]           | [1,1]         | [1,1,0] | []      |
| R05  | [1]       | [1,1,1,1,1,1] | [1]           | [1,1]         | [1,1,0] | []      |

dp = decision_results, ep = extra_results

- 观察:
  - 5轮结果完全一致，系统判定稳定
  - concept ep: 系统返回 [1,1,1,1,1,1]，GT 为 [1,0,0,1,1,1]，keyword_first_sentence 和 keyword_no_repeat 两项与 GT 不一致（系统判1，GT期望0）
  - application ep: 系统返回 [1,1]，GT 为 [1,0]，deduction_correct 与 GT 不一致（系统判1，GT期望0）
  - code dp: asr_match=0，与 GT 一致；系统正确短路，ep 为空
  - 注：GT 中 code passed 已从原始 True 修正为 False

- Metrics:

| 指标 | 公式 | 值 |
|------|------|----|
| 整体准确率 | matched_all / total_all = 10×5 / 13×5 = 50/65 | **76.92%** |
| 决定项准确率 | matched_dec / total_dec = 5×5 / 5×5 = 25/25 | **100.00%** |
| 加分项准确率 | matched_ext / total_ext = 5×5 / 8×5 = 25/40 | **62.50%** |
| 短路合规率 | compliant / applicable = 5/5 (code短路正确) | **100.00%** |

计算依据:
- 每轮判定点数: 决定项 5个, 加分项 8个 (concept:6 + application:2 + code:0短路), 共 13个
- 加分项每轮匹配: concept 4/6 + application 1/2 + code 0/0 = 5/8
- 加分项不匹配项: concept keyword_first_sentence(sys=1,GT=0), concept keyword_no_repeat(sys=1,GT=0), application deduction_correct(sys=1,GT=0)

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
| code | dp | asr_match | [0,0,0,0,0] | 0.0000 |

全部 13 个判定点 Gini = 0，完全稳定（尽管有3项与 GT 不一致，但系统自身判定完全稳定）。

---

算法工程师第三轮测试样本（Item 3）：
- 描述：三种题型都是错误样本 A-04 / C-04 / K-05
- 测试轮数： 5轮
- Ground Truth:
        concept: passed=False  决定项=[0]  加分项=[]（短路，define=0）
        application: passed=False  决定项=[0]  加分项=[]（短路，correct_option=0）
        code: passed=False  决定项=[1, 0, 0]  加分项=[]（短路，function_correct=0, asr_match=0）

- Testing Record:

| 轮次 | concept dp | concept ep | application dp | application ep | code dp | code ep |
|------|-----------|-----------|---------------|---------------|---------|---------|
| R01  | [0]       | []        | [0]           | []            | [0,0,0] | []      |
| R02  | [0]       | []        | [0]           | []            | [1,0,0] | []      |
| R03  | [0]       | []        | [0]           | []            | [1,0,0] | []      |
| R04  | [0]       | []        | [0]           | []            | [1,0,0] | []      |
| R05  | [0]       | []        | [0]           | []            | [0,0,0] | []      |

dp = decision_results, ep = extra_results

- 观察:
  - concept 和 application 5轮完全一致，与 GT 匹配
  - **code syntax_correct 出现波动**: R01/R05 判为0，R02/R03/R04 判为1，与 GT(=1) 不一致2轮
  - code function_correct 和 asr_match 5轮恒定为0，与 GT 一致
  - 三种题型均正确触发短路，ep 全部为空

- Metrics:

| 指标 | 公式 | 值 |
|------|------|----|
| 整体准确率 | matched_all / total_all = 23/25 | **92.00%** |
| 决定项准确率 | matched_dec / total_dec = 23/25 | **92.00%** |
| 加分项准确率 | N/A（三种题型均短路，无加分项可比较） | **N/A** |
| 短路合规率 | compliant / applicable = 15/15 (三种题型×5轮均正确短路) | **100.00%** |

计算依据:
- 每轮判定点数: 决定项 5个 (concept:1 + application:1 + code:3), 加分项 0个 (全部短路), 共 5个
- R01/R05: code syntax_correct=0, GT=1 → 各错1个 → 匹配 4/5
- R02/R03/R04: 全部与 GT 匹配 → 5/5
- 5轮总计: (4+5+5+5+4) = 23/25

- 样本判定稳定性 Gini Impurity（逐点）:

| 题型 | 类别 | 判定点 | 5轮序列 | G |
|------|------|--------|---------|---|
| concept | dp | define | [0,0,0,0,0] | 0.0000 |
| application | dp | correct_option | [0,0,0,0,0] | 0.0000 |
| code | dp | syntax_correct | [0,1,1,1,0] | **0.4800** |
| code | dp | function_correct | [0,0,0,0,0] | 0.0000 |
| code | dp | asr_match | [0,0,0,0,0] | 0.0000 |

**注意: code syntax_correct Gini = 1 - (3/5)² - (2/5)² = 1 - 0.36 - 0.16 = 0.4800，出现明显不稳定！**
这是首次观测到非零 Gini 值。K-05 样本的代码极度简化（仅3行，无查找逻辑），系统对其语法正确性的判定在不同轮次间出现波动。
