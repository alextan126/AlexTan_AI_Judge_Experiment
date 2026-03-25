通用岗第一轮测试样本（Item 1）：
- 描述：两种题型都是全对样本 A-01 / C-01（code_required=false）
- 测试轮数： 5轮
- Ground Truth:
        concept: passed=True  决定项=[1]  加分项=[1, 1, 1, 1, 1, 1]
        application: passed=True  决定项=[1]  加分项=[1, 1]

- Testing Record:

| 轮次 | concept dp | concept ep | application dp | application ep |
|------|-----------|-----------|---------------|---------------|
| R01  | [1]       | [1,1,1,1,1,1] | [1]           | [1,1]         |
| R02  | [1]       | [1,1,1,1,1,1] | [1]           | [1,1]         |
| R03  | [1]       | [1,1,1,1,1,1] | [1]           | [1,1]         |
| R04  | [1]       | [1,1,1,1,1,1] | [1]           | [1,1]         |
| R05  | [1]       | [1,1,1,1,1,1] | [1]           | [1,1]         |

dp = decision_results, ep = extra_results

- 观察: 5轮测试中所有判定点结果完全一致，与 Ground Truth 100% 匹配，无任何波动。

- Metrics:

| 指标 | 公式 | 值 |
|------|------|----|
| 整体准确率 | matched_all / total_all = 50/50 | **100.00%** |
| 决定项准确率 | matched_dec / total_dec = 10/10 | **100.00%** |
| 加分项准确率 | matched_ext / total_ext = 40/40 | **100.00%** |
| 短路合规率 | N/A（所有dp=1，无短路触发） | **N/A** |

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

---

通用岗第二轮测试样本（Item 2）：
- 描述：两种题型都是瑕疵样本 A-02 / C-02（code_required=false）
- 测试轮数： 5轮
- Ground Truth:
        concept: passed=True  决定项=[1]  加分项=[1, 0, 0, 1, 1, 1]
        application: passed=True  决定项=[1]  加分项=[1, 0]

- Testing Record:

| 轮次 | concept dp | concept ep | application dp | application ep |
|------|-----------|-----------|---------------|---------------|
| R01  | [1]       | [1,1,1,1,1,1] | [0]           | []            |
| R02  | [1]       | [1,1,1,1,1,1] | [0]           | []            |
| R03  | [1]       | [1,1,1,1,1,1] | [0]           | []            |
| R04  | [1]       | [1,1,1,1,1,1] | [0]           | []            |
| R05  | [1]       | [1,1,1,1,1,1] | [0]           | []            |

dp = decision_results, ep = extra_results

- 观察:
  - 5轮测试完全一致，无任何波动
  - concept dp: 与 GT 一致
  - concept ep: 系统返回 [1,1,1,1,1,1]，GT 为 [1,0,0,1,1,1]，**keyword_first_sentence** 和 **keyword_no_repeat** 两项与 GT 不一致（系统判1，GT期望0）
  - **application dp: 系统返回 correct_option=0，GT 期望=1，决定项判断错误！**
  - application ep: 因 correct_option=0 触发短路，ep=[]；GT 期望 ep=[1,0]

- Metrics:

| 指标 | 公式 | 值 |
|------|------|----|
| 整体准确率 | matched_all / total_all = 25/50 | **50.00%** |
| 决定项准确率 | matched_dec / total_dec = 5/10 | **50.00%** |
| 加分项准确率 | matched_ext / total_ext = 20/40 | **50.00%** |
| 短路合规率 | compliant / applicable = 5/5 (app dp=0时正确短路) | **100.00%** |

计算依据:
- 每轮GT判定点: 决定项 2个(concept:1 + app:1), GT加分项 8个(concept:6 + app:2), 共 10个
- 决定项每轮匹配: concept 1/1 + app 0/1 = 1/2 → 总计 5/10
- 加分项每轮匹配: concept 4/6(keyword_first_sentence和keyword_no_repeat不匹配) + app 0/2(短路无ep，GT期望[1,0]) = 4/8 → 总计 20/40
- 短路合规: app correct_option=0 触发短路，短路行为正确（GT期望correct_option=1是dp准确率问题）

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
| application | dp | correct_option | [0,0,0,0,0] | 0.0000 |

注意: application ep 因短路无数据，不计入 Gini 表。

---

通用岗第三轮测试样本（Item 3）：
- 描述：两种题型都是错误样本 A-04 / C-04（code_required=false）
- 测试轮数： 5轮
- Ground Truth:
        concept: passed=False  决定项=[0]  加分项=[]（短路，define=0）
        application: passed=False  决定项=[0]  加分项=[]（短路，correct_option=0）

- Testing Record:

| 轮次 | concept dp | concept ep | application dp | application ep |
|------|-----------|-----------|---------------|---------------|
| R01  | [0]       | []        | [0]           | []            |
| R02  | [0]       | []        | [0]           | []            |
| R03  | [0]       | []        | [0]           | []            |
| R04  | [0]       | []        | [0]           | []            |
| R05  | [0]       | []        | [0]           | []            |

dp = decision_results, ep = extra_results

- 观察: 5轮测试中所有判定点结果完全一致，与 Ground Truth 100% 匹配。两种题型均正确触发短路，加分项全部为空。

- Metrics:

| 指标 | 公式 | 值 |
|------|------|----|
| 整体准确率 | matched_all / total_all = 10/10 | **100.00%** |
| 决定项准确率 | matched_dec / total_dec = 10/10 | **100.00%** |
| 加分项准确率 | N/A（全部短路，无加分项） | **N/A** |
| 短路合规率 | compliant / applicable = 10/10 | **100.00%** |

- 样本判定稳定性 Gini Impurity（逐点）:

| 题型 | 类别 | 判定点 | 5轮序列 | G |
|------|------|--------|---------|---|
| concept | dp | define | [0,0,0,0,0] | 0.0000 |
| application | dp | correct_option | [0,0,0,0,0] | 0.0000 |
