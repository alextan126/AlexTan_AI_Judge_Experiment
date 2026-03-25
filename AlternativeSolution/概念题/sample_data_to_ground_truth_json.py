from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any


BASE_DIR = Path(__file__).resolve().parent
INPUT_PATH = BASE_DIR / "sampleData.md"
OUTPUT_PATH = BASE_DIR / "concept_ground_truth.json"

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

RAW_TO_CANONICAL_POINT_NAME = {
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

SECTION_RE = re.compile(r"^##\s+(.+?)\n(.*?)(?=^##\s+|\Z)", re.M | re.S)
POINT_LINE_RE = re.compile(r"([a-z_]+)（[^）]+）：\s*([01])（0/1）")


def _markdown_to_text(value: str) -> str:
    return value.replace(r"\|", "|").replace("<br>", "\n").strip()


def _parse_table_row(line: str) -> list[str]:
    parts = [part.strip() for part in line.strip().strip("|").split(" | ")]
    if len(parts) != 5:
        raise ValueError(f"Expected 5 columns in markdown table row, got {len(parts)}: {line}")
    return parts


def _parse_decision_points(decision_text: str, notes: str) -> tuple[list[dict[str, Any]], bool]:
    match = re.search(r"define（是否有定义）：\s*([01])（0/1）", decision_text)
    if not match:
        raise ValueError(f"Could not parse decision score from: {decision_text}")

    result = int(match.group(1))
    reason = notes or decision_text
    return (
        [
            {
                "name": "define",
                "desc": DECISION_POINT_DESCRIPTIONS["define"],
                "result": result,
                "reason": reason,
            }
        ],
        result == 1,
    )


def _parse_extra_points(extra_text: str, notes: str, passed: bool) -> list[dict[str, Any]]:
    if not passed:
        return []

    stripped = extra_text.strip()
    if not stripped or stripped == "/":
        return []

    points: list[dict[str, Any]] = []
    for name, result in POINT_LINE_RE.findall(stripped):
        canonical_name = RAW_TO_CANONICAL_POINT_NAME.get(name, name)
        points.append(
            {
                "name": canonical_name,
                "desc": EXTRA_POINT_DESCRIPTIONS.get(canonical_name, ""),
                "result": int(result),
                "reason": notes or stripped,
            }
        )

    expected_points = set(EXTRA_POINT_DESCRIPTIONS)
    found_points = {point["name"] for point in points}
    if found_points != expected_points:
        missing = sorted(expected_points - found_points)
        extra = sorted(found_points - expected_points)
        raise ValueError(
            f"Unexpected extra point set. Missing={missing}, extra={extra}, raw={extra_text}"
        )

    return points


def parse_sample_data(markdown_text: str) -> dict[str, Any]:
    sections = SECTION_RE.findall(markdown_text)
    if not sections:
        raise ValueError("No sample sections were found in sampleData.md")

    items: list[dict[str, Any]] = []
    item_index = 1

    for sample_file, section_body in sections:
        tester_match = re.search(r"^- tester:\s*(.+)$", section_body, re.M)
        question_match = re.search(r"^- question:\s*(.+)$", section_body, re.M)
        if not tester_match or not question_match:
            raise ValueError(f"Missing tester/question metadata in section: {sample_file}")

        tester = tester_match.group(1).strip()
        question = question_match.group(1).strip()

        table_rows = re.findall(r"^\|\s*C-\d{2}\s*\|.*$", section_body, re.M)
        if len(table_rows) != 5:
            raise ValueError(f"Expected 5 case rows in section {sample_file}, found {len(table_rows)}")

        for row_line in table_rows:
            case_id, decision_cell, extra_cell, answer_cell, note_cell = _parse_table_row(row_line)
            decision_text = _markdown_to_text(decision_cell)
            extra_text = _markdown_to_text(extra_cell)
            simulated_answer = _markdown_to_text(answer_cell)
            notes = _markdown_to_text(note_cell)

            decision_points, passed = _parse_decision_points(decision_text, notes)
            extra_points = _parse_extra_points(extra_text, notes, passed)

            items.append(
                {
                    "item_index": item_index,
                    "ability": question,
                    "sample_file": sample_file,
                    "tester": tester,
                    "question": question,
                    "case_id": case_id,
                    "simulated_answer": simulated_answer,
                    "notes": notes,
                    "concept": {
                        "decision_points": decision_points,
                        "passed": passed,
                        "extra_points": extra_points,
                        "model_cot": "",
                        "observation": None,
                        "raw_decision_text": decision_text,
                        "raw_bonus_text": extra_text,
                    },
                }
            )
            item_index += 1

    return {
        "sample_id": "concept_ground_truth",
        "description": "Human concept ground truth converted from sampleData.md",
        "source_markdown": str(INPUT_PATH),
        "total_items": len(items),
        "items": items,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Convert sampleData.md to concept ground-truth JSON")
    parser.add_argument("--input", default=str(INPUT_PATH), help="Path to sampleData.md")
    parser.add_argument("--output", default=str(OUTPUT_PATH), help="Output JSON path")
    args = parser.parse_args()

    input_path = Path(args.input)
    output_path = Path(args.output)

    payload = parse_sample_data(input_path.read_text(encoding="utf-8"))
    if payload["total_items"] != 25:
        raise ValueError(f"Expected 25 total items, found {payload['total_items']}")

    output_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {payload['total_items']} items to {output_path}")


if __name__ == "__main__":
    main()
