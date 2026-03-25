{
    "code": 200,
    "msg": "ok",
    "data": {
        "type": 2,
        "business_id": "123445555533",
        "data": {
            "items": [
                {
                    "item_index": 1,
                    "ability": "Java网络编程",

                    "concept": {
                        "decision_points": [
                            {"name": "define", "desc": "是否有定义", "result": 1, "reason": "候选人第一句即给出'线性表是…有限序列'的完整定义"}
                        ],
                        "passed": true,
                        "extra_points": [
                            {"name": "keyword", "desc": "关键词是否存在", "result": 1, "reason": "回答中包含关键词'线性表'"},
                            {"name": "keyword_first_sentence", "desc": "关键词是否在第一句", "result": 1, "reason": "第一句即出现'线性表'"},
                            {"name": "keyword_no_repeat", "desc": "是否未重复关键词", "result": 0, "reason": "候选人在第二、三句中重复提及关键词"},
                            {"name": "not_overtime", "desc": "答题时间是否在标准答案1.5倍内", "result": 1, "reason": "作答时长未超标"},
                            {"name": "define_first_sentence", "desc": "定义是否在第一句", "result": 1, "reason": "第一句包含完整定义"},
                            {"name": "order_define_explain", "desc": "顺序是否是定义+解释", "result": 1, "reason": "先定义后解释，结构清晰"}
                        ],
                        "model_cot": "reasoning_content原文...",
                        "observation": {
                            "direction": "pro",
                            "ability_tag": "概念表达清晰度",
                            "behavior_reason": "候选人在回答概念题时，第一句即给出完整定义，随后条理清晰地展开解释...",
                            "ai_observation": "系统观察到候选人具备扎实的基础概念储备和良好的表达组织能力。"
                        }
                    },

                    "application": {
                        "decision_points": [
                            {"name": "correct_option", "desc": "是否选对了", "result": 0, "reason": "候选人选择了链表而非正确答案顺序表"}
                        ],
                        "passed": false,
                        "extra_points": [],
                        "model_cot": "reasoning_content原文...",
                        "observation": {
                            "direction": "con",
                            "ability_tag": "场景分析能力",
                            "behavior_reason": "在 Q2（应用题）中，候选人选择了链表而非顺序表，未能准确识别题目中'随机访问'的核心需求...",
                            "ai_observation": "系统观察到候选人在将理论知识映射到实际场景时，需求抓取能力有所欠缺。"
                        }
                    },

                    "code": {
                        "decision_points": [
                            {"name": "syntax_correct", "desc": "语法是否正确", "result": 1, "reason": "代码无语法错误，可正常运行"},
                            {"name": "function_correct", "desc": "功能是否实现", "result": 1, "reason": "删除第3个元素后输出与预期一致"},
                            {"name": "asr_match", "desc": "ASR逻辑的对应性", "result": 1, "reason": "口述思路与代码实现逻辑一致"}
                        ],
                        "passed": true,
                        "extra_points": [
                            {"name": "time_optimal", "desc": "是否Tn最佳", "result": 1, "reason": "时间复杂度为O(n)，已是最优"},
                            {"name": "space_optimal", "desc": "是否Sn最佳", "result": 0, "reason": "使用了额外列表拷贝，空间非最优"},
                            {"name": "code_readability", "desc": "代码可读性", "result": 1, "reason": "变量命名清晰，结构分明"},
                            {"name": "comment_readability", "desc": "注释可读性", "result": 1, "reason": "关键步骤均有注释说明"}
                        ],
                        "model_cot": "reasoning_content原文...",
                        "observation": {
                            "direction": "pro",
                            "ability_tag": "工程编码能力",
                            "behavior_reason": "候选人在 Q3（代码题）中代码结构清晰，口述思路与代码逻辑一致...",
                            "ai_observation": "系统观察到候选人具备扎实的基础概念储备和良好的表达组织能力。"
                        }
                    }
                },
                ......
            ]
        }
    }
}

## Normally item_index = 7  -> 通常有7道题

Output 字段说明：

顶层字段：
字段	类型	说明
code	int	HTTP 状态码，200 表示成功
msg	string	状态消息
data	object	回调数据体

data 层：
字段	类型	说明
type	int	MAS 类型标识 (固定为 2)
business_id	str	业务 ID，与请求时传入的一致
data	object	评审结果数据

data.data.items[] 层（每个题组）：
字段	类型	说明
item_index	int	题目编号 [1 - item_num]
ability	string	该题对应的能力标签
concept	object	概念题评审结果
application	object	应用题评审结果
code	object?	代码题评审结果 (无代码题岗为 null)

题型对象 (concept / application / code) 内部结构：
字段	类型	说明
decision_points	array	决定项判定结果列表
passed	boolean	决定项是否全部通过 (true=通过, false=未通过)
extra_points	array	额外判定项结果列表；若 passed=false 则为空数组 []
model_cot	string	该题型 Agent 的模型 reasoning_content 原文 (CoT 链式推理过程)
observation	object?	主观观察结果（未观察到素质能力特征时为 null）

decision_points[] / extra_points[] 元素：
字段	类型	说明
name	string	判定项标识名 (如 "define", "correct_option", "syntax_correct" 等)
desc	string	判定项描述
result	int	判定结果：1=通过, 0=未通过
reason	string	AI 给出判 0/1 的理由说明

observation 对象：
字段	类型	说明
direction	string	观察方向："pro" (表现出色) 或 "con" (有待提升)
ability_tag	string	LLM 动态生成的能力标签 (如 "概念表达清晰度", "场景分析能力" 等)
behavior_reason	string	基于候选人作答行为的具体分析说明
ai_observation	string	AI 综合观察总结