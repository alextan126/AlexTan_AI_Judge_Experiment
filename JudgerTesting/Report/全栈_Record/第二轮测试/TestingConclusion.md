第二轮测试样本：
- 描述：三种题型都是瑕疵样本 A-02 / C-02 / K-02
- 测试轮数： 10轮
- Ground Truth:
        concept: passed=True  决定项=[1]  加分项=[1, 0, 0, 1, 1, 1]
        application: passed=True  决定项=[1]  加分项=[1, 0]
        code: passed=True  决定项=[1, 1, 0]  加分项=[]

- Testing Record:

| 轮次 | concept dp | concept ep | application dp | application ep | code dp | code ep |
|------|-----------|-----------|---------------|---------------|---------|---------|
| R01  | [1]       | [1,0,1,1,1,1] | [1]           | [1,0]         | [1,1,0] | [] |
| R02  | [1]       | [1,0,1,1,1,1] | [1]           | [1,0]         | [1,1,0] | [] |
| R03  | [1]       | [1,0,1,1,1,1] | [1]           | [1,0]         | [1,1,0] | [] |
| R04  | [1]       | [1,0,1,1,1,1] | [1]           | [1,0]         | [1,1,0] | [] |
| R05  | [1]       | [1,0,1,1,1,1] | [1]           | [1,0]         | [1,1,0] | [] |
| R06  | [1]       | [1,0,1,1,1,1] | [1]           | [1,0]         | [1,1,0] | [] |
| R07  | [1]       | [1,0,1,1,1,1] | [1]           | [1,0]         | [1,1,0] | [] |
| R08  | [1]       | [1,0,1,1,1,1] | [1]           | [1,0]         | [1,1,0] | [] |
| R09  | [1]       | [1,0,1,1,1,1] | [1]           | [1,0]         | [1,1,0] | [] |
| R10  | [1]       | [1,0,1,1,1,1] | [1]           | [1,0]         | [1,1,0] | [] |

dp = decision_results, ep = extra_results

- 观察: 10轮测试中所有判定点结果完全一致，无任何波动。
  与 GT 对比存在 1 处偏差: concept ep 第3项 keyword_no_repeat 系统判为1，GT期望0。

- Metrics:

| 指标 | 公式 | 值 |
|------|------|----|
| 整体准确率 | matched_all / total_all = 12×10 / 13×10 = 120/130 | **92.31%** |
| 决定项准确率 | matched_dec / total_dec = 5×10 / 5×10 = 50/50 | **100.00%** |
| 加分项准确率 | matched_ext / total_ext = 7×10 / 8×10 = 70/80 | **87.50%** |
| 短路合规率 | code dp含0 → ep应为[] → 系统ep=[] → 10/10 | **100.00%** |

计算依据:
- 每轮判定点数: 决定项 5个 (concept:1 + application:1 + code:3), 加分项 8个 (concept:6 + application:2 + code:0 短路), 共 13个
- 决定项: 全部 5 项与 GT 一致 (define=1, correct_option=1, syntax_correct=1, function_correct=1, asr_match=0)
- 加分项: 8 项中 7 项与 GT 一致, keyword_no_repeat 系统=1 vs GT=0 → 每轮 miss 1
- 短路合规: code 的 asr_match=0 导致 passed=false, 系统正确返回 ep=[], 合规

- 样本判定稳定性 Gini Impurity（逐点）:

| 题型 | 类别 | 判定点 | 10轮序列 | G |
|------|------|--------|----------|---|
| concept | dp | define | [1,1,1,1,1,1,1,1,1,1] | 0.0000 |
| concept | ep | keyword | [1,1,1,1,1,1,1,1,1,1] | 0.0000 |
| concept | ep | keyword_first_sentence | [0,0,0,0,0,0,0,0,0,0] | 0.0000 |
| concept | ep | keyword_no_repeat | [1,1,1,1,1,1,1,1,1,1] | 0.0000 |
| concept | ep | not_overtime | [1,1,1,1,1,1,1,1,1,1] | 0.0000 |
| concept | ep | define_first_sentence | [1,1,1,1,1,1,1,1,1,1] | 0.0000 |
| concept | ep | order_define_explain | [1,1,1,1,1,1,1,1,1,1] | 0.0000 |
| application | dp | correct_option | [1,1,1,1,1,1,1,1,1,1] | 0.0000 |
| application | ep | hook_original | [1,1,1,1,1,1,1,1,1,1] | 0.0000 |
| application | ep | deduction_correct | [0,0,0,0,0,0,0,0,0,0] | 0.0000 |
| code | dp | syntax_correct | [1,1,1,1,1,1,1,1,1,1] | 0.0000 |
| code | dp | function_correct | [1,1,1,1,1,1,1,1,1,1] | 0.0000 |
| code | dp | asr_match | [0,0,0,0,0,0,0,0,0,0] | 0.0000 |
| code | ep | (短路，无额外判定) | — | — |

全部 13 个判定点 Gini = 0，完全稳定。keyword_no_repeat 虽然与 GT 不一致，但 10 轮中判定恒定为 1，属于"稳定的错误判定"。


-- 分析结论：
    所有轮统一的判错点：| concept | ep | keyword_no_repeat | [1,1,1,1,1,1,1,1,1,1] | 0.0000 |
    专家的回答如下：
        它是一种以资源为核心、通过统一接口规范来组织网络请求的 Web 接口设计方式。RESTful API 强调把业务对象抽象成资源，RESTful API 通常会使用 URL 表示资源，并结合不同的 HTTP 方法完成对应操作，所以这样  的设计更容易理解和维护。
    AI的推理：
            {
                "name": "keyword_no_repeat",
                "desc": "候选人是否未过度重复关键词",
                "result": 1,
                "reason": "关键词“RESTful API”在回答中出现了两次，属于正常使用，没有过度重复。"
            },

    人工结论：AI的判断是对的，专家是错的。