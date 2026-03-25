第三轮测试样本：
- 描述：三种题型都是错误样本 A-04 / C-04 / K-05
- 测试轮数： 10轮
- Ground Truth:
        concept: passed=False  决定项=[0]  加分项=[]
        application: passed=False  决定项=[0]  加分项=[]
        code: passed=False  决定项=[1, 0, 0]  加分项=[]

- Testing Record:

| 轮次 | concept dp | concept ep | application dp | application ep | code dp | code ep |
|------|-----------|-----------|---------------|---------------|---------|---------|
| R01  | [0]       | []        | [0]           | []            | [1,0,0] | [] |
| R02  | [0]       | []        | [0]           | []            | [1,0,0] | [] |
| R03  | [0]       | []        | [0]           | []            | [1,0,0] | [] |
| R04  | [0]       | []        | [0]           | []            | [1,0,0] | [] |
| R05  | [0]       | []        | [0]           | []            | [1,0,0] | [] |
| R06  | [0]       | []        | [0]           | []            | [1,0,0] | [] |
| R07  | [0]       | []        | [0]           | []            | [1,0,0] | [] |
| R08  | [0]       | []        | [0]           | []            | [1,0,0] | [] |
| R09  | [0]       | []        | [0]           | []            | [1,0,0] | [] |
| R10  | [0]       | []        | [0]           | []            | [1,0,0] | [] |

dp = decision_results, ep = extra_results

- 观察: 10轮测试中所有判定点结果完全一致，与 Ground Truth 100% 匹配，无任何波动。三种题型决定项不通过时均正确触发短路，ep 全部为空。

- Metrics:

| 指标 | 公式 | 值 |
|------|------|----|
| 整体准确率 | matched_all / total_all = 5×10 / 5×10 = 50/50 | **100.00%** |
| 决定项准确率 | matched_dec / total_dec = 5×10 / 5×10 = 50/50 | **100.00%** |
| 加分项准确率 | N/A (GT 全短路，无加分项) | **100.00%** (vacuous truth) |
| 短路合规率 | concept(dp=0→ep=[])✓ + application(dp=0→ep=[])✓ + code(dp含0→ep=[])✓ = 30/30 | **100.00%** |

计算依据:
- 每轮判定点数: 决定项 5个 (concept:1 + application:1 + code:3), 加分项 0个 (全短路), 共 5个
- 决定项: 全部 5 项与 GT 一致 (define=0, correct_option=0, syntax_correct=1, function_correct=0, asr_match=0)
- 短路合规: 三种题型均有 dp=0，系统全部返回 ep=[]，3×10=30 次短路全部合规

- 样本判定稳定性 Gini Impurity（逐点）:

| 题型 | 类别 | 判定点 | 10轮序列 | G |
|------|------|--------|----------|---|
| concept | dp | define | [0,0,0,0,0,0,0,0,0,0] | 0.0000 |
| application | dp | correct_option | [0,0,0,0,0,0,0,0,0,0] | 0.0000 |
| code | dp | syntax_correct | [1,1,1,1,1,1,1,1,1,1] | 0.0000 |
| code | dp | function_correct | [0,0,0,0,0,0,0,0,0,0] | 0.0000 |
| code | dp | asr_match | [0,0,0,0,0,0,0,0,0,0] | 0.0000 |
| concept | ep | (短路，无额外判定) | — | — |
| application | ep | (短路，无额外判定) | — | — |
| code | ep | (短路，无额外判定) | — | — |

全部 5 个判定点 Gini = 0，完全稳定。