import os
import re
import json
from pathlib import Path
from typing import Any

try:
    from langchain_core.messages import HumanMessage, SystemMessage
    from langchain_openai import ChatOpenAI
except ImportError:
    raise ImportError("Please install langchain-openai and langchain-core")

BASE_DIR = Path(__file__).resolve().parents[2]
INPUT_DIR = BASE_DIR / "JudgerTesting" / "Samples" / "全栈工程师" / "应用题"
OUTPUT_DIR = BASE_DIR / "JudgerTesting" / "NewSample" / "全栈工程师" / "应用题"

DEFAULT_MODEL = os.getenv("CONCEPT_JUDGER_MODEL", "gpt-4o-mini")

def _build_llm() -> ChatOpenAI:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is required.")

    kwargs: dict[str, Any] = {
        "api_key": api_key,
        "model": DEFAULT_MODEL,
        "temperature": 0.7,
        "max_retries": 2,
    }

    base_url = os.getenv("OPENAI_BASE_URL")
    if base_url:
        kwargs["base_url"] = base_url

    return ChatOpenAI(**kwargs)

def extract_metadata(content: str) -> tuple[str, str]:
    tester_match = re.search(r"测试人：(.+)", content)
    question_match = re.search(r"题目：\n(.+?)(?=\n\n|\Z)", content, re.S)
    
    tester = tester_match.group(1).strip() if tester_match else "未知"
    question = question_match.group(1).strip() if question_match else ""
    
    return tester, question

def generate_cases(llm: ChatOpenAI, question: str) -> list[dict[str, str]]:
    system_prompt = (
        "你是一个资深的技术面试官，需要为一道全栈工程师的应用题生成5个不同质量的模拟候选人回答。\n"
        "我们采用 STARE 框架进行评分：\n"
        "- S (Situation) / T (Task): 转述问题。成功描述清楚问题，并转述成功。\n"
        "- A (Action): 二选一选择方案。选择对的方案。\n"
        "- R (Result): (做什么) 该方案解决什么问题，带来什么好处。正确回答该方案的好处。\n"
        "- E (Evaluation): (为什么) 该方案为什么能解决问题，带来好处。在正确回答的基础上，给出对应的分析，并且分析正确。\n\n"
        "请生成以下 5 种类型的回答，并以 JSON 数组格式返回（不要包含 Markdown 代码块，直接返回合法的 JSON 数组）：\n"
        "[\n"
        "  {\n"
        '    "case_id": "A-01",\n'
        '    "stare_level": "STARE",\n'
        '    "score": 3,\n'
        '    "answer": "...",\n'
        '    "notes": "..."\n'
        "  },\n"
        "  ...\n"
        "]\n\n"
        "5个Case的要求如下：\n"
        "1. STARE (3分) - 完美的标准答案：包含完整的 STARE 元素，逻辑严密，分析透彻。\n"
        "2. STAR (2分) - 知其然不知其所以然型答案：能正确选择方案，并指出方案的好处，但缺乏底层的原理解释（缺少 E）。\n"
        "3. STA (1分) - 有根据的猜测型答案：能转述问题并选对方案，但给不出具体的好处和原理解释（缺少 R 和 E）。\n"
        "4. ST/Others (0分) - 只能转述问题，选错方案：转述了问题，但是选错了方案，后续解释也是基于错误方案的。\n"
        "5. Others (0分) - 完全答非所问或全错：没有转述问题，选错方案，或者回答完全不相关的内容。\n"
    )
    
    user_prompt = f"题目：\n{question}\n\n请生成 5 个模拟回答。"
    
    response = llm.invoke([
        SystemMessage(content=system_prompt),
        HumanMessage(content=user_prompt)
    ])
    
    content = response.content
    if isinstance(content, str):
        content = content.strip()
        if content.startswith("```"):
            content = re.sub(r"^```(?:json)?\s*", "", content)
            content = re.sub(r"\s*```$", "", content)
        try:
            return json.loads(content)
        except json.JSONDecodeError as e:
            print(f"Failed to parse JSON: {content}")
            raise e
    return []

def format_markdown(tester: str, question: str, cases: list[dict[str, str]]) -> str:
    md = f"甄才AI测试问卷 - 全栈工程师 - 应用题\n"
    md += f"岗位：全栈工程师\n"
    md += f"测试人：{tester}\n\n"
    md += f"说明：\n"
    md += f"- 模拟候选人回答区为测试人填写区\n"
    md += f"- 备注区可以稍微填写故意设计的思路\n\n"
    md += f"题型：应用题\n"
    md += f"题目：\n{question}\n\n"
    
    for case in cases:
        md += f"\n样本测试序号 {case['case_id']}\n"
        md += f"STARE_level: {case['stare_level']} / score: {case['score']}\n\n"
        md += f"模拟候选人回答：\n{case['answer']}\n\n"
        md += f"备注：\n{case['notes']}\n\n"
        md += f"————————\n"
        
    return md

def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    llm = _build_llm()
    
    for file_path in sorted(INPUT_DIR.glob("FullStack_Sample*.md")):
        print(f"Processing {file_path.name}...")
        content = file_path.read_text(encoding="utf-8")
        tester, question = extract_metadata(content)
        
        if not question:
            print(f"Could not extract question from {file_path.name}")
            continue
            
        cases = generate_cases(llm, question)
        
        output_content = format_markdown(tester, question, cases)
        output_path = OUTPUT_DIR / file_path.name
        output_path.write_text(output_content, encoding="utf-8")
        print(f"Saved {output_path.name}")

if __name__ == "__main__":
    main()
