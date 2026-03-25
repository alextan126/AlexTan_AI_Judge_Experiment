# Linux/WSL-compatible request

cat > request.json <<'JSON'
{
  "type": 2,
  "business_id": "201002121221",
  "callback": "https://webhook.site/55a8c52e-b7ba-4b24-ae34-0f510a05bc19",
  "data": {
    "code_required": true,
    "item_num": 1,
    "items": [
      {
        "item_index": 1,
        "ability": "Java网络编程",
        "knowledge": "线性表的定义：线性表是具有相同数据类型的n个数据元素的有限序列",
        "concept_keyword": "线性表",
        "concept_question": "请给出线性表的定义，请简洁描述",
        "concept_standard_answer": "线性表是具有相同数据类型的n(n>=0)个数据元素的有限序列",
        "concept_rubric": "R1评分标准：决定点-是否有定义；额外点-关键词是否存在、关键词是否在第一句",
        "concept_user_answer": "线性表是具有相同数据类型的n个数据元素的有限序列",
        "application_question": "假设你正在开发一个日志系统，你会选择顺序表还是链表？请说明理由",
        "application_correct_option": "顺序表",
        "application_standard_answer": "选择顺序表。尾部追加O(1)，随机访问O(1)，缓存友好",
        "application_rubric": "R2评分标准：决定点-是否选对了；额外点-是否挂钩原题、是否推导正确",
        "application_user_answer": "我会选择顺序表作为底层存储结构，因为日志是顺序追加的",
        "code_question": "请用代码实现一个线性表，支持初始化和删除操作",
        "code_standard_answer": "初始化[a1,a2,a3,a4,a5]，删除第3个元素a3后变为[a1,a2,a4,a5]",
        "code_rubric": "R3评分标准：决定点-语法是否正确、功能是否实现；额外点-时间复杂度最优、空间复杂度最优",
        "code_user_answer": "思路是先用列表初始化线性表，然后用pop删除指定位置元素",
        "code_user_code": "def linear_list_operations():\n    L = ['a1', 'a2', 'a3', 'a4', 'a5']\n    L.pop(2)\n    return L"
      },
    ]
  }
}
JSON

curl -X POST 'http://localhost:8000/api/v1/agent/exam' \
  -H 'Content-Type: application/json' \
  --data-binary '@request.json'