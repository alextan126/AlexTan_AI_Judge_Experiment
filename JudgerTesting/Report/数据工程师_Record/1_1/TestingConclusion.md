数据工程师第一轮测试样本：
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
| 整体准确率 | matched_all / total_all = (5+12)×5 / (5+12)×5 = 85/85 | **100.00%** |
| 决定项准确率 | matched_dec / total_dec = 5×5 / 5×5 = 25/25 | **100.00%** |
| 加分项准确率 | matched_ext / total_ext = 12×5 / 12×5 = 60/60 | **100.00%** |
| 短路合规率 | compliant / applicable = N/A (GT全Pass，无短路场景) | **100.00%** (vacuous truth) |

计算依据:
- 每轮判定点数: 决定项 5个 (concept:1 + application:1 + code:3), 加分项 12个 (concept:6 + application:2 + code:4), 共 17个
- 5轮 × 17点 = 85个判定，全部与 Ground Truth 一致
- 短路合规: GT 三种题型 passed 均为 True，不存在决定项=0的场景，按惯例记为 100%

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



数据工程师第二轮测试样本：
- 描述：三种题型都是瑕疵样本 A-02 / C-02 / K-02
- 测试轮数： 5轮
- Ground Truth:
        concept: passed=True  决定项=[1]  加分项=[1, 0, 0, 1, 1, 1]
        application: passed=True  决定项=[1]  加分项=[1, 0]
        code: passed=False  决定项=[1, 1, 0]  加分项=[]（短路，asr_match=0）

- Testing Record:

| 轮次 | concept dp | concept ep | application dp | application ep | code dp | code ep |
|------|-----------|-----------|---------------|---------------|---------|---------|
| R01  | [1]       | [1,1,1,1,1,1] | [1]           | [1,0]         | [1,1,0] | []      |
| R02  | [1]       | [1,1,1,1,1,1] | [1]           | [1,0]         | [1,1,0] | []      |
| R03  | [1]       | [1,1,1,1,1,1] | [1]           | [1,0]         | [1,1,0] | []      |
| R04  | [1]       | [1,1,1,1,1,1] | [1]           | [1,0]         | [1,1,0] | []      |
| R05  | [1]       | [1,1,1,1,1,1] | [1]           | [1,0]         | [1,1,0] | []      |

dp = decision_results, ep = extra_results

- 观察:
  - 5轮结果完全一致，无任何波动
  - concept ep: 系统返回 [1,1,1,1,1,1]，GT 为 [1,0,0,1,1,1]，keyword_first_sentence 和 keyword_no_repeat 两项与 GT 不一致（系统判1，GT期望0）
  - application ep: deduction_correct=0，与 GT 一致（推导含错误事实）
  - code dp: asr_match=0，与 GT 一致（口述说递归，代码用循环）；系统正确短路，ep 为空
  - 注：GT 中 code passed 已从原始 True 修正为 False（决定项存在0时 passed 应为 False）

- Metrics:

| 指标 | 公式 | 值 |
|------|------|----|
| 整体准确率 | matched_all / total_all = 11×5 / 13×5 = 55/65 | **84.62%** |
| 决定项准确率 | matched_dec / total_dec = 5×5 / 5×5 = 25/25 | **100.00%** |
| 加分项准确率 | matched_ext / total_ext = 6×5 / 8×5 = 30/40 | **75.00%** |
| 短路合规率 | compliant / applicable = 5/5 (code短路正确) | **100.00%** |

计算依据:
- 每轮判定点数: 决定项 5个 (concept:1 + application:1 + code:3), 加分项 8个 (concept:6 + application:2 + code:0短路), 共 13个
- 决定项: 全部与 GT 一致 → 25/25
- 加分项: concept ep 中 keyword_first_sentence(sys=1,GT=0) 和 keyword_no_repeat(sys=1,GT=0) 每轮各错2个 → 每轮匹配 6/8 → 5轮 30/40
- 短路合规: code 决定项含0，系统返回 passed=False 且 ep=[]，短路行为正确

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
| application | ep | deduction_correct | [0,0,0,0,0] | 0.0000 |
| code | dp | syntax_correct | [1,1,1,1,1] | 0.0000 |
| code | dp | function_correct | [1,1,1,1,1] | 0.0000 |
| code | dp | asr_match | [0,0,0,0,0] | 0.0000 |

全部 13 个判定点 Gini = 0，完全稳定（尽管 concept ep 中有2项与 GT 不一致，但系统自身判定完全稳定）。



数据工程师第三轮测试样本：
- 描述：三种题型都是错误样本 A-04 / C-04 / K-05
- 测试轮数： 5轮
- Ground Truth:
        concept: passed=False  决定项=[0]  加分项=[]（短路，define=0）
        application: passed=False  决定项=[0]  加分项=[]（短路，correct_option=0）
        code: passed=False  决定项=[1, 0, 0]  加分项=[]（短路，function_correct=0, asr_match=0）

- Testing Record:

| 轮次 | concept dp | concept ep | application dp | application ep | code dp | code ep |
|------|-----------|-----------|---------------|---------------|---------|---------|
| R01  | [0]       | []        | [0]           | []            | [1,0,0] | []      |
| R02  | [0]       | []        | [0]           | []            | [1,0,0] | []      |
| R03  | [0]       | []        | [0]           | []            | [1,0,0] | []      |
| R04  | [0]       | []        | [0]           | []            | [1,0,0] | []      |
| R05  | [0]       | []        | [0]           | []            | [1,0,0] | []      |

dp = decision_results, ep = extra_results

- 观察: 5轮测试中所有判定点结果完全一致，与 Ground Truth 100% 匹配，无任何波动。三种题型均正确触发短路，加分项全部为空。

- Metrics:

| 指标 | 公式 | 值 |
|------|------|----|
| 整体准确率 | matched_all / total_all = 5×5 / 5×5 = 25/25 | **100.00%** |
| 决定项准确率 | matched_dec / total_dec = 5×5 / 5×5 = 25/25 | **100.00%** |
| 加分项准确率 | N/A（三种题型均短路，无加分项可比较） | **N/A** |
| 短路合规率 | compliant / applicable = 15/15 (三种题型×5轮均正确短路) | **100.00%** |

计算依据:
- 每轮判定点数: 决定项 5个 (concept:1 + application:1 + code:3), 加分项 0个 (全部短路), 共 5个
- 5轮 × 5点 = 25个判定，全部与 Ground Truth 一致
- 短路合规: concept(define=0)、application(correct_option=0)、code(function_correct=0,asr_match=0) 三种题型均含决定项=0，系统全部返回 passed=False 且 ep=[]，短路行为正确，5轮×3题型=15次检查全部合规

- 样本判定稳定性 Gini Impurity（逐点）:

| 题型 | 类别 | 判定点 | 5轮序列 | G |
|------|------|--------|---------|---|
| concept | dp | define | [0,0,0,0,0] | 0.0000 |
| application | dp | correct_option | [0,0,0,0,0] | 0.0000 |
| code | dp | syntax_correct | [1,1,1,1,1] | 0.0000 |
| code | dp | function_correct | [0,0,0,0,0] | 0.0000 |
| code | dp | asr_match | [0,0,0,0,0] | 0.0000 |

全部 5 个判定点 Gini = 0，完全稳定。
