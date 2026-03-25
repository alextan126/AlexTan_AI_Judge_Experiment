{
    "type": 2,
    "business_id": "201002121221",
    "callback": "https://platform.example.com/api/callback",
    "data": {
        "code_required": true,
        "item_num": 1,
        "items": [
            {
                "item_index": 1,
                "ability": "Java网络编程",
                "knowledge": "1. 线性表的定义 (Definition)...",

                "concept_keyword": "线性表",
                "concept_question": "请给出线性表的定义...,请简洁描述",
                "concept_standard_answer": "线性表是具有相同数据类型的n(n≥0)个数据元素的有限序列...",
                "concept_rubric": "R1评分标准：决定点-是否有定义；额外点-关键词是否存在、关键词是否在第一句...",
                "concept_user_answer": "线性表是具有相同数据类型的n个数据元素的有限序列...",

                "application_question": "假设你正在开发一个日志系统...你会选择「顺序表」还是「链表」？请说明理由",
                "application_correct_option": "顺序表",
                "application_standard_answer": "选择顺序表。尾部追加O(1)，随机访问O(1)...",
                "application_rubric": "R2评分标准：决定点-是否选对了；额外点-是否挂钩原题、是否推导正确",
                "application_user_answer": "我会选择顺序表作为底层存储结构...",

                "code_question": "请用代码实现一个线性表...",
                "code_standard_answer": "初始化[a1,a2,a3,a4,a5]，删除第3个元素a3后变为[a1,a2,a4,a5]...",
                "code_rubric": "R3评分标准：决定点-语法是否正确、功能是否实现、ASR逻辑对应性；额外点-Tn最佳、Sn最佳、代码可读性、注释可读性",
                "code_user_answer": "思路是先用列表初始化线性表...",
                "code_user_code": "def linear_list_operations():\n    L = ['a1', 'a2', 'a3', 'a4', 'a5']\n    ..."
            },
            ........

        ]
    }
}


Input 字段说明：

顶层字段：
字段	类型	必填	说明
type	int	是	MAS 类型标识 (固定为 2，代表 ReviewMicroMAS)
business_id	str	是	业务 ID，用于关联请求与回调
callback	string	是	回调地址，MAS 处理完成后将结果 POST 到此 URL
data	object	是	请求数据体

data 层：
字段	类型	必填	说明
code_required	boolean	是	是否需要代码题 Agent (true=需要，false=跳过代码题评审)
item_num	int	是	题目数量
items	array	是	题组列表，包含 1-7 个题组对象

data.items[] 层（每个题组）：
字段	类型	必填	说明
item_index	int	是	题目编号[1 - item_num]
ability	string	是	该题对应的能力标签
knowledge	string	是	知识源片段 (K)
concept_keyword	string	是	概念题关键词，用于评判概念题回答
concept_question	string	是	Q1 概念题题面
concept_standard_answer	string	是	Q1A 概念题标准答案
concept_rubric	string	是	Q1 概念题评分标准 (R1)
concept_user_answer	string	是	考生概念题 ASR 口述答案
application_question	string	是	Q2 应用题题面
application_correct_option	string	是	Q2 正确选项
application_standard_answer	string	是	Q2A 应用题标准答案
application_rubric	string	是	Q2 应用题评分标准 (R2)
application_user_answer	string	是	考生应用题 ASR 口述答案
code_question	string?	否	Q3 代码题题面 (无代码题岗为 null)
code_standard_answer	string?	否	Q3 标准答案/预期输出
code_rubric	string?	否	Q3 代码题评分标准 (R3)
code_user_answer	string?	否	考生代码题 ASR 口述解题思路
code_user_code	string?	否	考生代码题提交的代码