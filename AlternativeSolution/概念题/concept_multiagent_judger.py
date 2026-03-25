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
    "keyword": "关键词是否存在",
    "keyword_first_sentence": "关键词是否在第一句",
    "keyword_no_repeat": "是否未重复关键词",
    "not_overtime": "答题时间是否在标准答案1.5倍内",
    "define_first_sentence": "定义是否在第一句",
    "order_define_explain": "顺序是否是定义+解释",
}

BONUS_POINT_ORDER = list(EXTRA_POINT_DESCRIPTIONS.keys())

BONUS_POINT_GUIDANCE = {
    "keyword": (
        "judge semantic subject presence rather than exact token matching: pass only when "
        "the answer clearly names the core subject or a direct semantic equivalent instead "
        "of relying on vague pronouns, indirect references, or a long绕圈子的 lead-in."
    ),
    "keyword_first_sentence": (
        "judge semantic directness in the first sentence: pass only when the first sentence "
        "already introduces the core subject or a direct semantic equivalent; fail when the "
        "first sentence is mostly background, filler, examples, or indirect setup."
    ),
    "keyword_no_repeat": (
        "judge semantic conciseness rather than literal repetition counts: pass when the "
        "core subject is established once and the rest of the answer naturally elaborates; "
        "fail when later sentences redundantly restate the same core subject or its close "
        "semantic equivalent in a repetitive, unnatural way."
    ),
    "not_overtime": (
        "use answer length and verbosity as a proxy; concise answers pass, overly long "
        "rambling answers fail."
    ),
    "define_first_sentence": (
        "pass only when the actual defining statement appears in the first sentence, rather "
        "than starting with background or examples."
    ),
    "order_define_explain": (
        "pass only when the answer defines first and explains after."
    ),
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
        "You are the decision agent for a Chinese concept-question judging workflow. "
        "Judge only the decision point `define` and extract the candidate's own core "
        "definition phrase if the answer contains a definition. "
        "Return JSON only with this shape: "
        '{"define": 0 or 1, "reason": "...", "key_definition": "..."}.\n'
        "Rules:\n"
        "- `define=1` only when the answer clearly states what the concept is.\n"
        "- `key_definition` must be a short phrase copied or tightly paraphrased from "
        "the user's answer, such as `Web 接口设计风格`.\n"
        "- If `define=0`, return an empty string for `key_definition`.\n"
        "- Do not judge bonus points in this step."
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
        "You are an independent bonus-point judging agent for a Chinese concept-question "
        "workflow. Judge exactly one point and return JSON only with this shape: "
        '{"name": "...", "result": 0 or 1, "reason": "..."}.\n'
        "Use the extracted key definition from the decision agent as the anchor for the "
        "core concept. Make a strict 0/1 judgment for the requested point only.\n"
        "Important: for the three `keyword*` points, do semantic judging instead of exact "
        "string matching. Treat close paraphrases as the same concept, but do not reward "
        "answers that stay vague or repeatedly restate the same idea.\n"
        "Point-specific guidance:\n"
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
            returned_name = str(point_payload.get("name", point_name)).strip() or point_name
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
