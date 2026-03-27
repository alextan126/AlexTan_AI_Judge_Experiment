from __future__ import annotations

import argparse
import json
import os
import re
from pathlib import Path
from typing import Any

try:
    from langchain_core.messages import HumanMessage, SystemMessage
    from langchain_openai import ChatOpenAI
except ImportError as exc:  # pragma: no cover - depends on local environment
    ChatOpenAI = None  # type: ignore[assignment]
    HumanMessage = None  # type: ignore[assignment]
    SystemMessage = None  # type: ignore[assignment]
    LANGCHAIN_IMPORT_ERROR = exc
else:
    LANGCHAIN_IMPORT_ERROR = None


DECISION_POINT_DESCRIPTIONS = {
    "define": "是否有定义",
}

EXTRA_POINT_DESCRIPTIONS = {
    "semantic_clarity": "语义明确性",
    "semantic_directness": "开门见山",
    "semantic_conciseness": "语义精炼/不啰嗦",
    "not_overtime": "答题时间是否在标准答案1.5倍内",
    "define_first_sentence": "定义是否在第一句",
    "order_define_explain": "顺序是否是定义+解释",
}

BONUS_POINT_ORDER = list(EXTRA_POINT_DESCRIPTIONS.keys())

BONUS_POINT_GUIDANCE = {
    "semantic_clarity": (
        "判断“语义明确性”，回答中是否明确点出了题目所问核心概念，"
        "或者用了直接等价的语义表达，就可以判 1；如果回答始终使用“它”“这种方式”"
        "“这个东西”之类模糊指代，或者一直绕圈子不明确点题，则判 0。"
    ),
    "semantic_directness": (
        "判断“开门见山”。第一句是否直接引出题目所问核心概念，"
        "或者给出直接等价的语义表达，就判 1；如果第一句主要是在铺垫背景、说废话、举例子、"
        "绕弯子，没有直接点题，则判 0。"
    ),
    "semantic_conciseness": (
        "判断“语义精炼/不啰嗦”，回答在明确点题后，后续内容是否是对概念的有效补充。后续内容是"
        "自然展开解释，没有反复用不同说法重复同一个核心概念，就判 1；如果回答多次重复表达"
        "同一个核心概念，语义上显得啰嗦、车轱辘话明显，则判 0。"
    ),
    "not_overtime": (
        "用回答长度和冗长度作为近似标准；简洁、控制在合理篇幅内判 1，明显过长、啰嗦、"
        "离题扩写严重则判 0。"
    ),
    "define_first_sentence": (
        "回答是否只在第一句就给出真正且正确的定义。给出时判 1；如果先讲背景、举例子、铺垫，再下定义，则判 0。"
    ),
    "order_define_explain": (
        "回答是否遵循总分总或者总分的有逻辑的答题顺序。若在回答时有逻辑，如先给定义在举例子判 1；"
        "如果回答正确但无逻辑，东一句西一句，则判 0。"
    ),
}

POINT_NAME_ALIASES = {
    "keyword": "semantic_clarity",
    "keyword_first_sentence": "semantic_directness",
    "keyword_no_repeat": "semantic_conciseness",
    "semantic_clarity": "semantic_clarity",
    "semantic_directness": "semantic_directness",
    "semantic_conciseness": "semantic_conciseness",
    "not_overtime": "not_overtime",
    "define_first_sentence": "define_first_sentence",
    "order_define_explain": "order_define_explain",
}

DEFAULT_MODEL = os.getenv("CONCEPT_JUDGER_MODEL", "gpt-4.1-mini")
DEFAULT_TIMEOUT = float(os.getenv("CONCEPT_JUDGER_TIMEOUT", "60"))


class JudgerError(RuntimeError):
    """Raised when the multi-agent judging flow cannot complete."""


def _ensure_langchain() -> None:
    if LANGCHAIN_IMPORT_ERROR is not None:
        raise JudgerError(
            "LangChain dependencies are missing. Install `langchain-openai` and "
            "`langchain-core` before running this script."
        ) from LANGCHAIN_IMPORT_ERROR


def _build_llm() -> ChatOpenAI:
    _ensure_langchain()

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise JudgerError("OPENAI_API_KEY is required to run the concept judger.")

    kwargs: dict[str, Any] = {
        "api_key": api_key,
        "model": DEFAULT_MODEL,
        "temperature": 0,
        "timeout": DEFAULT_TIMEOUT,
        "max_retries": 2,
    }

    base_url = os.getenv("OPENAI_BASE_URL")
    if base_url:
        kwargs["base_url"] = base_url

    return ChatOpenAI(**kwargs)


def _normalize_message_content(content: Any) -> str:
    if isinstance(content, str):
        return content

    if isinstance(content, list):
        parts: list[str] = []
        for chunk in content:
            if isinstance(chunk, str):
                parts.append(chunk)
            elif isinstance(chunk, dict):
                text = chunk.get("text")
                if isinstance(text, str):
                    parts.append(text)
        return "\n".join(part for part in parts if part)

    return str(content)


def _extract_json_object(text: str) -> dict[str, Any]:
    cleaned = text.strip()
    if cleaned.startswith("```"):
        cleaned = re.sub(r"^```(?:json)?\s*", "", cleaned)
        cleaned = re.sub(r"\s*```$", "", cleaned)

    try:
        payload = json.loads(cleaned)
    except json.JSONDecodeError:
        match = re.search(r"\{.*\}", cleaned, re.S)
        if not match:
            raise JudgerError(f"Model did not return valid JSON: {text}")
        try:
            payload = json.loads(match.group(0))
        except json.JSONDecodeError as exc:
            raise JudgerError(f"Model returned malformed JSON: {text}") from exc

    if not isinstance(payload, dict):
        raise JudgerError(f"Model JSON must be an object, got: {type(payload).__name__}")

    return payload


def _invoke_json_agent(llm: ChatOpenAI, system_prompt: str, user_prompt: str) -> dict[str, Any]:
    response = llm.invoke(
        [
            SystemMessage(content=system_prompt),
            HumanMessage(content=user_prompt),
        ]
    )
    content = _normalize_message_content(response.content)
    return _extract_json_object(content)


def _first_sentence(text: str) -> str:
    stripped = text.strip()
    if not stripped:
        return ""

    match = re.search(r"^(.+?[。！？!?])(?:\s|$)", stripped, re.S)
    if match:
        return match.group(1).strip()

    first_line = stripped.splitlines()[0].strip()
    return first_line


def _decision_agent_prompt(question: str, user_answer: str) -> tuple[str, str]:
    system_prompt = (
        "你是中文概念题评分流程中的 decision agent。你只负责判断决定项 `define`，"
        "并在回答包含定义时，提取出候选人自己表述的核心定义短语。"
        "你必须且只能返回如下格式的 JSON："
        '{"define": 0 or 1, "reason": "...", "key_definition": "..."}.\n'
        "规则：\n"
        "- `define=1`：只有当回答清晰地陈述了该概念是什么时才给 1 分。\n"
        "- `key_definition`：必须是从用户回答中复制或紧密改写的简短短语。\n"
        "- 如果 `define=0`，则 `key_definition` 返回空字符串。\n"
        "- 在这一步不要判断任何加分项。"
    )
    user_prompt = (
        f"Question:\n{question}\n\n"
        f"User answer:\n{user_answer}\n"
    )
    return system_prompt, user_prompt


def _bonus_agent_prompt(
    point_name: str,
    point_desc: str,
    question: str,
    user_answer: str,
    key_definition: str,
) -> tuple[str, str]:
    system_prompt = (
        "你是中文概念题评分流程中的独立加分项评审 agent。你一次只判断一个点，"
        "并且只能返回如下 JSON："
        '{"name": "...", "result": 0 or 1, "reason": "..."}.\n'
        "使用 decision agent 抽取出的 key definition 作为核心概念锚点。"
        "你只对当前请求的单个点做严格的 0/1 判断。\n"
        f"`name` 字段必须返回当前点位名 `{point_name}`，不要改写成其他别名。\n"
        "当前点位说明：\n"
        f"- `{point_name}`: {BONUS_POINT_GUIDANCE[point_name]}"
    )
    user_prompt = (
        f"Point name: {point_name}\n"
        f"Point description: {point_desc}\n"
        f"Extracted key definition: {key_definition}\n"
        f"First sentence: {_first_sentence(user_answer)}\n\n"
        f"Question:\n{question}\n\n"
        f"User answer:\n{user_answer}\n"
    )
    return system_prompt, user_prompt


def _build_point_result(name: str, result: int, reason: str) -> dict[str, Any]:
    desc = DECISION_POINT_DESCRIPTIONS.get(name) or EXTRA_POINT_DESCRIPTIONS.get(name, "")
    return {
        "name": name,
        "desc": desc,
        "result": int(result),
        "reason": reason.strip(),
    }


def _normalize_binary(value: Any, field_name: str) -> int:
    if value in (0, 1):
        return int(value)
    if isinstance(value, bool):
        return int(value)
    if isinstance(value, str) and value.strip() in {"0", "1"}:
        return int(value.strip())
    raise JudgerError(f"Field `{field_name}` must be 0 or 1, got: {value!r}")


def _canonicalize_point_name(name: str) -> str:
    normalized = name.strip()
    return POINT_NAME_ALIASES.get(normalized, normalized)


def judge_concept_answer(
    *,
    question: str,
    user_answer: str,
    item_index: int = 1,
    ability: str | None = None,
    sample_file: str | None = None,
    case_id: str | None = None,
) -> dict[str, Any]:
    llm = _build_llm()

    decision_system, decision_user = _decision_agent_prompt(question, user_answer)
    decision_payload = _invoke_json_agent(llm, decision_system, decision_user)

    define_result = _normalize_binary(decision_payload.get("define"), "define")
    decision_reason = str(decision_payload.get("reason", "")).strip()
    key_definition = str(decision_payload.get("key_definition", "")).strip()
    if define_result == 0:
        key_definition = ""

    decision_points = [
        _build_point_result("define", define_result, decision_reason or "No reason provided.")
    ]

    extra_points: list[dict[str, Any]] = []
    if define_result == 1:
        for point_name in BONUS_POINT_ORDER:
            system_prompt, user_prompt = _bonus_agent_prompt(
                point_name,
                EXTRA_POINT_DESCRIPTIONS[point_name],
                question,
                user_answer,
                key_definition,
            )
            point_payload = _invoke_json_agent(llm, system_prompt, user_prompt)
            result = _normalize_binary(point_payload.get("result"), point_name)
            reason = str(point_payload.get("reason", "")).strip() or "No reason provided."
            returned_name = _canonicalize_point_name(
                str(point_payload.get("name", point_name)).strip() or point_name
            )
            if returned_name != point_name:
                raise JudgerError(
                    f"Point agent returned `{returned_name}` but `{point_name}` was expected."
                )
            extra_points.append(_build_point_result(point_name, result, reason))

    result = {
        "item_index": item_index,
        "ability": ability or question,
        "sample_file": sample_file,
        "case_id": case_id,
        "question": question,
        "simulated_answer": user_answer,
        "concept": {
            "decision_points": decision_points,
            "passed": define_result == 1,
            "extra_points": extra_points,
            "model_cot": "",
            "observation": None,
            "extracted_definition": key_definition,
        },
    }
    return result


def _load_payload_from_args(args: argparse.Namespace) -> dict[str, Any]:
    if args.input_json:
        payload = json.loads(Path(args.input_json).read_text(encoding="utf-8"))
        if not isinstance(payload, dict):
            raise JudgerError("`--input-json` must contain a JSON object.")
        return payload

    if not args.question or not args.answer:
        raise JudgerError("Provide `--question` and `--answer`, or use `--input-json`.")

    return {
        "question": args.question,
        "user_answer": args.answer,
        "item_index": args.item_index,
        "ability": args.ability,
        "sample_file": args.sample_file,
        "case_id": args.case_id,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="LangChain multi-agent concept judger")
    parser.add_argument("--question", help="Concept question text")
    parser.add_argument("--answer", help="Candidate answer text")
    parser.add_argument("--item-index", type=int, default=1, help="Item index for output JSON")
    parser.add_argument("--ability", help="Ability label to include in the output")
    parser.add_argument("--sample-file", help="Optional sample file name metadata")
    parser.add_argument("--case-id", help="Optional case id metadata")
    parser.add_argument("--input-json", help="Path to a JSON payload with question/user_answer")
    parser.add_argument("--output", help="Optional output JSON file path")
    args = parser.parse_args()

    payload = _load_payload_from_args(args)
    result = judge_concept_answer(
        question=str(payload["question"]),
        user_answer=str(payload["user_answer"]),
        item_index=int(payload.get("item_index", 1)),
        ability=payload.get("ability"),
        sample_file=payload.get("sample_file"),
        case_id=payload.get("case_id"),
    )

    rendered = json.dumps(result, ensure_ascii=False, indent=2)
    if args.output:
        Path(args.output).write_text(rendered + "\n", encoding="utf-8")
    else:
        print(rendered)


if __name__ == "__main__":
    try:
        main()
    except JudgerError as exc:
        raise SystemExit(f"[error] {exc}")
