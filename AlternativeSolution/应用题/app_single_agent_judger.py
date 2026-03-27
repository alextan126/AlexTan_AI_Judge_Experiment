import os
import json
from typing import Any, Dict, Optional
from pydantic import BaseModel, Field

try:
    from langchain_core.messages import HumanMessage, SystemMessage
    from langchain_openai import ChatOpenAI
except ImportError:
    raise ImportError("Please install langchain-openai and langchain-core")

DEFAULT_MODEL = os.getenv("APP_SOTA_MODEL", "gpt-5.4")

class SingleAgentOutput(BaseModel):
    stare_level: str = Field(description="STARE 等级 (STARE, STAR, STA, ST/Others, A, Others)")
    score: int = Field(description="分数 (3, 2, 1, 0)")
    reasoning: str = Field(description="评分理由")

def _build_llm() -> ChatOpenAI:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is required.")

    kwargs: dict[str, Any] = {
        "api_key": api_key,
        "model": DEFAULT_MODEL,
        "temperature": 0.0,
        "max_retries": 2,
    }

    base_url = os.getenv("OPENAI_BASE_URL")
    if base_url:
        kwargs["base_url"] = base_url

    return ChatOpenAI(**kwargs)

_system_prompt = """你是一个资深的技术面试官，负责对全栈工程师的应用题回答进行评分。
面试者采用 STARE 框架回答，我们也对应评分，请根据以下标准对候选人的回答进行评判：

STARE 框架定义：
- S (Situation) / T (Task): 转述题目中描述的问题。面试者要成功描述清楚问题，说明要做的任务。
- A (Action): 二选一选择方案。选择对的方案。面试者要选中正确答案。
- R (Result - 知其然): 候选人仅仅陈述了该方案带来的**表面影响或直接结果**（例如：“速度更快”、“并发更高”、“避免全表扫描”、“Redis比MySQL快”）。
- E (Evaluation - 知其所以然): 候选人对**为什么**会产生这个结果进行了**底层机制的分析**或**深度的架构权衡(trade-off)**。必须触及技术原理（例如：“因为行锁降低了锁粒度”、“因为 B+ 树的 O(logN) 特性”、“因为内存操作削峰并异步落盘减少 I/O”）。

STARE 评级与分数（从好到坏）：
- STARE (3分): 完美的标准答案。包含 S/T, A, R, E。
- STAR (2分): 知其然不知其所以然型答案。能正确地选择，并且意识到正确方案的核心优势，却不知道其优势的底层逻辑。包含 S/T, A, R，缺少 E。
- STA (1分): 有根据的猜测型答案。能完整地转述，并且有根据地猜测出正确答案，但不能提供任何证据。包含 S/T, A，缺少 R, E。
- ST/Others (0分): 只能转述问题，选错方案。包含 S/T，但 A 选错。
- A (0分): 仅给出选项，没有转述问题。包含 A，缺少 S/T。
- Others (0分): 其余 (ST/A/ARE/AR)，不得分，如不能完成前三步（即 STA），即可视为乱蒙，乱猜，瞎说。

【评分示例】
题目：高并发下数据库自增 ID 成为瓶颈，选 A (UUID) 还是 B (雪花算法)？
正确答案：方案 B

候选人回答 1 (评级：STAR - 2分):
“现在高并发下数据库自增 ID 是瓶颈（S/T）。我选方案 B 雪花算法（A）。因为雪花算法生成的 ID 也是唯一的，而且它生成速度非常快，不会像数据库自增那样卡顿，所以能解决并发问题（R）。”
-> 评分理由：包含了 S/T, A, R。但缺少 E，因为只说了“速度快、不卡顿”这个表面结果（R），没有解释底层机制。

候选人回答 2 (评级：STARE - 3分):
“现在高并发下数据库自增 ID 是瓶颈（S/T）。我选方案 B 雪花算法（A）。因为雪花算法生成的 ID 也是唯一的，而且它生成速度非常快，能解决并发问题（R）。底层的核心原因是：雪花算法是在应用层本地内存中通过时间戳、机器码和序列号进行位运算生成的，完全不需要网络 I/O 去请求数据库，从而彻底消除了数据库单点锁竞争的瓶颈（E）。”
-> 评分理由：包含了 S/T, A, R，并且详细解释了“为什么快”（本地内存位运算、消除单点锁竞争），满足了 E。

请仔细阅读题目、正确答案和候选人的回答，分析其包含哪些 STARE 元素，并给出最终的评级和分数。
"""

def judge_app_answer_single(question: str, answer: str, correct_answer: str) -> Dict[str, Any]:
    """
    使用单个 Agent 评估应用题回答。
    """
    llm = _build_llm()
    structured_llm = llm.with_structured_output(SingleAgentOutput)
    
    user_prompt = f"【题目】\n{question}\n\n【正确答案】\n{correct_answer}\n\n【候选人回答】\n{answer}\n\n请给出评分。"
    
    try:
        result: SingleAgentOutput = structured_llm.invoke([
            SystemMessage(content=_system_prompt),
            HumanMessage(content=user_prompt)
        ])
        
        return {
            "stare_level": result.stare_level,
            "score": result.score,
            "reasoning": result.reasoning
        }
    except Exception as e:
        print(f"Error in single agent judger: {e}")
        return {
            "stare_level": "Error",
            "score": 0,
            "reasoning": str(e)
        }

if __name__ == "__main__":
    # Test
    q = "某系统查询慢，方案A加索引，方案B不加。选哪个？"
    c = "方案A"
    a = "我选A，因为加索引能变快，解决查询慢的问题。底层是因为B+树能降低复杂度。"
    print(json.dumps(judge_app_answer_single(q, a, c), indent=2, ensure_ascii=False))
