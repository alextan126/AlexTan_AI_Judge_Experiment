import os
import json
import concurrent.futures
from typing import Any, Dict
from pydantic import BaseModel, Field

try:
    from langchain_core.messages import HumanMessage, SystemMessage
    from langchain_openai import ChatOpenAI
except ImportError:
    raise ImportError("Please install langchain-openai and langchain-core")

DEFAULT_MODEL = os.getenv("APP_MINI_MODEL", "gpt-4.1-mini")

class ComponentOutput(BaseModel):
    passed: bool = Field(description="是否满足该项标准")
    reasoning: str = Field(description="判断理由")

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

def _evaluate_component(llm: ChatOpenAI, component: str, description: str, question: str, answer: str) -> Dict[str, Any]:
    structured_llm = llm.with_structured_output(ComponentOutput)
    
    system_prompt = f"""你是一个资深的技术面试官，负责对全栈工程师的应用题回答进行局部评分。
你需要判断候选人的回答是否满足 STARE 框架中的【{component}】标准。

【{component}】的标准定义：
{description}

请仔细阅读题目和候选人的回答，判断其是否满足该标准，并给出理由。
"""
    
    user_prompt = f"【题目】\n{question}\n\n【候选人回答】\n{answer}\n\n请判断是否满足【{component}】标准。"
    
    try:
        result: ComponentOutput = structured_llm.invoke([
            SystemMessage(content=system_prompt),
            HumanMessage(content=user_prompt)
        ])
        return {
            "component": component,
            "passed": result.passed,
            "reasoning": result.reasoning
        }
    except Exception as e:
        print(f"Error evaluating {component}: {e}")
        return {
            "component": component,
            "passed": False,
            "reasoning": f"Error: {str(e)}"
        }

def judge_app_answer_multi(question: str, answer: str) -> Dict[str, Any]:
    """
    使用多个 Agent 并行评估应用题回答的各个部分，然后通过程序逻辑组装结果。
    """
    llm = _build_llm()
    
    components = [
        {
            "name": "S/T (Situation/Task)",
            "desc": "转述问题。成功描述清楚问题，并转述成功。"
        },
        {
            "name": "A (Action)",
            "desc": "二选一选择方案。选择对的方案。注意：必须选对方案才算通过。"
        },
        {
            "name": "R (Result)",
            "desc": "(做什么) 该方案解决什么问题，带来什么好处。正确回答该方案的好处。"
        },
        {
            "name": "E (Evaluation)",
            "desc": "(为什么) 该方案为什么能解决问题，带来好处。在正确回答的基础上，给出对应的分析，并且分析正确。"
        }
    ]
    
    results = {}
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
        future_to_comp = {
            executor.submit(_evaluate_component, llm, comp["name"], comp["desc"], question, answer): comp["name"]
            for comp in components
        }
        for future in concurrent.futures.as_completed(future_to_comp):
            comp_name = future_to_comp[future]
            try:
                res = future.result()
                # Use simplified keys for logic
                key = comp_name.split(" ")[0] # S/T, A, R, E
                results[key] = res
            except Exception as exc:
                print(f"{comp_name} generated an exception: {exc}")
                results[comp_name.split(" ")[0]] = {"passed": False, "reasoning": "Error"}

    # Programmatic Aggregation
    has_st = results.get("S/T", {}).get("passed", False)
    has_a = results.get("A", {}).get("passed", False)
    has_r = results.get("R", {}).get("passed", False)
    has_e = results.get("E", {}).get("passed", False)
    
    stare_level = "Others"
    score = 0
    
    if not has_st and has_a:
        stare_level = "A"
        score = 0
    elif has_st and not has_a:
        stare_level = "ST/Others"
        score = 0
    elif has_st and has_a and not has_r:
        stare_level = "STA"
        score = 1
    elif has_st and has_a and has_r and not has_e:
        stare_level = "STAR"
        score = 2
    elif has_st and has_a and has_r and has_e:
        stare_level = "STARE"
        score = 3
    else:
        stare_level = "Others"
        score = 0
        
    return {
        "stare_level": stare_level,
        "score": score,
        "components": results,
        "reasoning": f"S/T: {has_st}, A: {has_a}, R: {has_r}, E: {has_e}"
    }

if __name__ == "__main__":
    # Test
    q = "某系统查询慢，方案A加索引，方案B不加。选哪个？"
    a = "我选A，因为加索引能变快，解决查询慢的问题。底层是因为B+树能降低复杂度。"
    print(json.dumps(judge_app_answer_multi(q, a), indent=2, ensure_ascii=False))
