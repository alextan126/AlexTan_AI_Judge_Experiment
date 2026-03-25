第一轮测试样本：
- 描述：三种题型都是全对样本 A-01 / C-01 / K-01
- 测试轮数： 10轮
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
| R06  | [1]       | [1,1,1,1,1,1] | [1]           | [1,1]         | [1,1,1] | [1,1,1,1] |
| R07  | [1]       | [1,1,1,1,1,1] | [1]           | [1,1]         | [1,1,1] | [1,1,1,1] |
| R08  | [1]       | [1,1,1,1,1,1] | [1]           | [1,1]         | [1,1,1] | [1,1,1,1] |
| R09  | [1]       | [1,1,1,1,1,1] | [1]           | [1,1]         | [1,1,1] | [1,1,1,1] |
| R10  | [1]       | [1,1,1,1,1,1] | [1]           | [1,1]         | [1,1,1] | [1,1,1,1] |

dp = decision_results, ep = extra_results

- 观察: 10轮测试中所有判定点结果完全一致，与 Ground Truth 100% 匹配，无任何波动。

- Metrics:

| 指标 | 公式 | 值 |
|------|------|----|
| 整体准确率 | matched_all / total_all = (5+12)×10 / (5+12)×10 = 170/170 | **100.00%** |
| 决定项准确率 | matched_dec / total_dec = 5×10 / 5×10 = 50/50 | **100.00%** |
| 加分项准确率 | matched_ext / total_ext = 12×10 / 12×10 = 120/120 | **100.00%** |
| 短路合规率 | compliant / applicable = N/A (GT全Pass，无短路场景) | **100.00%** (vacuous truth) |

计算依据:
- 每轮判定点数: 决定项 5个 (concept:1 + application:1 + code:3), 加分项 12个 (concept:6 + application:2 + code:4), 共 17个
- 10轮 × 17点 = 170个判定，全部与 Ground Truth 一致
- 短路合规: GT 三种题型 passed 均为 True，不存在决定项=0的场景，按惯例记为 100%

- 样本判定稳定性 Gini Impurity（逐点）:

| 题型 | 类别 | 判定点 | 10轮序列 | G |
|------|------|--------|----------|---|
| concept | dp | define | [1,1,1,1,1,1,1,1,1,1] | 0.0000 |
| concept | ep | keyword | [1,1,1,1,1,1,1,1,1,1] | 0.0000 |
| concept | ep | keyword_first_sentence | [1,1,1,1,1,1,1,1,1,1] | 0.0000 |
| concept | ep | keyword_no_repeat | [1,1,1,1,1,1,1,1,1,1] | 0.0000 |
| concept | ep | not_overtime | [1,1,1,1,1,1,1,1,1,1] | 0.0000 |
| concept | ep | define_first_sentence | [1,1,1,1,1,1,1,1,1,1] | 0.0000 |
| concept | ep | order_define_explain | [1,1,1,1,1,1,1,1,1,1] | 0.0000 |
| application | dp | correct_option | [1,1,1,1,1,1,1,1,1,1] | 0.0000 |
| application | ep | hook_original | [1,1,1,1,1,1,1,1,1,1] | 0.0000 |
| application | ep | deduction_correct | [1,1,1,1,1,1,1,1,1,1] | 0.0000 |
| code | dp | syntax_correct | [1,1,1,1,1,1,1,1,1,1] | 0.0000 |
| code | dp | function_correct | [1,1,1,1,1,1,1,1,1,1] | 0.0000 |
| code | dp | asr_match | [1,1,1,1,1,1,1,1,1,1] | 0.0000 |
| code | ep | time_optimal | [1,1,1,1,1,1,1,1,1,1] | 0.0000 |
| code | ep | space_optimal | [1,1,1,1,1,1,1,1,1,1] | 0.0000 |
| code | ep | code_readability | [1,1,1,1,1,1,1,1,1,1] | 0.0000 |
| code | ep | comment_readability | [1,1,1,1,1,1,1,1,1,1] | 0.0000 |

全部 17 个判定点 Gini = 0，完全稳定。