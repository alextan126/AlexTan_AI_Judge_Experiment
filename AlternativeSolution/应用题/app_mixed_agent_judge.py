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

DEFAULT_MODEL = os.getenv("APP_SOTA_MODEL", "gpt-5.4")

class MainAgentOutput(BaseModel):
    has_st: bool = Field(description="是否满足 S/T (Situation/Task) 标准")
    has_a: bool = Field(description="是否满足 A (Action) 标准")
    has_r: bool = Field(description="是否满足 R (Result) 标准")
    has_e: bool = Field(description="是否满足 E (Evaluation) 标准")
    reasoning: str = Field(description="整体评分理由")

class VoterOutput(BaseModel):
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

def _run_main_agent(llm: ChatOpenAI, question: str, answer: str, correct_answer: str) -> Dict[str, Any]:
    structured_llm = llm.with_structured_output(MainAgentOutput)
    
    system_prompt = """你是一个资深的技术面试官，负责对工程师的应用题回答进行基础评分。
请判断候选人的回答是否包含以下 STARE 元素：

- S/T (Situation/Task): 转述题目中描述的问题。面试者要成功描述清楚问题，说明要做的任务。
- A (Action): 二选一选择方案。选择对的方案。面试者要选中正确答案。
- R (Result): 候选人陈述了该方案带来的表面影响或直接结果（例如：“速度更快”、“并发更高”、“避免全表扫描”）。
- E (Evaluation): 候选人对为什么会产生这个结果进行了底层机制的分析或深度的架构权衡。
  【注意】：只要候选人给出了合理的底层机制解释（如“行锁将锁粒度控制在数据行级别”、“复杂度降至 O(√N)”、“通过二级索引表定位数据块”等），或者进行了合理的对比分析，就应当判定为满足 E。不要对 E 的标准过于苛刻。
"""
    
    user_prompt = f"【题目】\n{question}\n\n【正确答案】\n{correct_answer}\n\n【候选人回答】\n{answer}\n\n请判断包含哪些元素。"
    
    try:
        result: MainAgentOutput = structured_llm.invoke([
            SystemMessage(content=system_prompt),
            HumanMessage(content=user_prompt)
        ])
        return {
            "has_st": result.has_st,
            "has_a": result.has_a,
            "has_r": result.has_r,
            "has_e": result.has_e,
            "reasoning": result.reasoning
        }
    except Exception as e:
        print(f"Error in main agent: {e}")
        return {"has_st": False, "has_a": False, "has_r": False, "has_e": False, "reasoning": str(e)}

def _run_voter(llm: ChatOpenAI, voter_name: str, prompt_angle: str, question: str, answer: str) -> Dict[str, Any]:
    structured_llm = llm.with_structured_output(VoterOutput)
    
    system_prompt = f"""你是一个专门负责评估技术面试回答中特定维度的评审员。
你的任务是根据以下特定视角，判断候选人的回答是否达标：

【评估视角】：{prompt_angle}

请仔细阅读题目和候选人的回答，给出你的判断（True/False）和理由。
"""
    
    user_prompt = f"【题目】\n{question}\n\n【候选人回答】\n{answer}\n\n请根据你的评估视角给出判断。"
    
    try:
        result: VoterOutput = structured_llm.invoke([
            SystemMessage(content=system_prompt),
            HumanMessage(content=user_prompt)
        ])
        return {
            "voter_name": voter_name,
            "passed": result.passed,
            "reasoning": result.reasoning
        }
    except Exception as e:
        print(f"Error in {voter_name}: {e}")
        return {"voter_name": voter_name, "passed": False, "reasoning": str(e)}

def judge_app_answer_mixed(question: str, answer: str, correct_answer: str) -> Dict[str, Any]:
    """
    使用 Mixed-Agent 架构评估应用题回答。
    Main Agent (2 votes) + 3 R-Voters (1 vote each) + 3 E-Voters (1 vote each).
    """
    llm = _build_llm()
    
    voters_config = [
        {"name": "R-Voter-1", "angle": "候选人是否明确陈述了其所选方案带来的直接好处或表面影响（例如：速度变快了、内存节省了等）？"},
        {"name": "R-Voter-2", "angle": "候选人是否提及了其所选方案是如何解决题目中描述的具体业务问题的？"},
        {"name": "R-Voter-3", "angle": "候选人是否在结果层面上指出其方案比另一个方案更好、更快或更有效率？"},
        {"name": "E-Voter-1", "angle": "候选人是否提及了任何底层的技术机制、算法复杂度或数据结构特性（例如：O(N)、锁粒度、磁盘I/O等）？"},
        {"name": "E-Voter-2", "angle": "候选人是否对两个方案进行了技术层面的 Trade-off（权衡/利弊）分析？"},
        {"name": "E-Voter-3", "angle": "候选人是否成功解释了方案“为什么”有效，而不仅仅是说它有效？注意：只要解释正确且触及了一定深度的技术原理，即算通过。"}
    ]
    
    results = {}
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=7) as executor:
        # Submit Main Agent
        future_main = executor.submit(_run_main_agent, llm, question, answer, correct_answer)
        
        # Submit Voters
        future_to_voter = {
            executor.submit(_run_voter, llm, v["name"], v["angle"], question, answer): v["name"]
            for v in voters_config
        }
        
        main_result = future_main.result()
        results["Main_Agent"] = main_result
        
        for future in concurrent.futures.as_completed(future_to_voter):
            voter_name = future_to_voter[future]
            try:
                results[voter_name] = future.result()
            except Exception as exc:
                print(f"{voter_name} generated an exception: {exc}")
                results[voter_name] = {"voter_name": voter_name, "passed": False, "reasoning": "Error"}

    # Tally Votes
    r_votes = 0
    e_votes = 0
    
    if main_result.get("has_r"):
        r_votes += 2
    if main_result.get("has_e"):
        e_votes += 2
        
    for i in range(1, 4):
        if results.get(f"R-Voter-{i}", {}).get("passed"):
            r_votes += 1
        if results.get(f"E-Voter-{i}", {}).get("passed"):
            e_votes += 1
            
    final_st = main_result.get("has_st", False)
    final_a = main_result.get("has_a", False)
    final_r = r_votes >= 4
    final_e = e_votes >= 4
    
    stare_level = "Others"
    score = 0
    
    if not final_st and final_a:
        stare_level = "A"
        score = 0
    elif final_st and not final_a:
        stare_level = "ST/Others"
        score = 0
    elif final_st and final_a and not final_r:
        stare_level = "STA"
        score = 1
    elif final_st and final_a and final_r and not final_e:
        stare_level = "STAR"
        score = 2
    elif final_st and final_a and final_r and final_e:
        stare_level = "STARE"
        score = 3
    else:
        stare_level = "Others"
        score = 0
        
    return {
        "stare_level": stare_level,
        "score": score,
        "components": results,
        "vote_tally": {
            "R_votes": r_votes,
            "E_votes": e_votes,
            "threshold": 4
        },
        "reasoning": f"S/T: {final_st}, A: {final_a}, R({r_votes}/5): {final_r}, E({e_votes}/5): {final_e}. Main Agent Reasoning: {main_result.get('reasoning')}"
    }

if __name__ == "__main__":
    # Test
    q = "某系统查询慢，方案A加索引，方案B不加。选哪个？"
    c = "方案A"
    a = "我选A，因为加索引能变快，解决查询慢的问题。底层是因为B+树能降低复杂度。"
    print(json.dumps(judge_app_answer_mixed(q, a, c), indent=2, ensure_ascii=False))