from __future__ import annotations

import re
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
SOURCE_DIR = REPO_ROOT / "JudgerTesting" / "Samples" / "全栈工程师" / "概念题"
OUTPUT_PATH = Path(__file__).resolve().parent / "sampleData.md"

CASE_RE = re.compile(r"样本测试序号\s*(C-\d{2})")


def normalize_text(text: str) -> str:
    return text.replace("\r\n", "\n").replace("\u3000", " ").replace("\xa0", " ")


def extract_single_line(text: str, label: str) -> str:
    match = re.search(rf"{re.escape(label)}\s*[：:]\s*(.+)", text)
    if not match:
        raise ValueError(f"Could not find field: {label}")
    return match.group(1).strip()


def extract_question(text: str) -> str:
    match = re.search(r"Q1\s*题面：\s*\n(.*?)(?:\n\s*\n)*样本测试序号", text, re.S)
    if not match:
        raise ValueError("Could not find question text")
    return " ".join(line.strip() for line in match.group(1).splitlines() if line.strip())


def clean_section(text: str) -> str:
    cleaned_lines = [line.rstrip() for line in text.strip().splitlines()]
    while cleaned_lines and cleaned_lines[-1].strip("—- ").strip() == "":
        cleaned_lines.pop()
    while cleaned_lines and cleaned_lines[-1].strip() in {"————————", "----------------"}:
        cleaned_lines.pop()
    return "\n".join(cleaned_lines).strip()


def extract_section(block: str, start_label: str, end_labels: list[str]) -> str:
    start_pattern = rf"^\s*{re.escape(start_label)}[^\n]*[：:](.*?(?:\n|$))"
    if end_labels:
        end_pattern = rf"(?=^\s*(?:{'|'.join(re.escape(label) + r'[^\n]*' for label in end_labels)})[：:]|\Z)"
    else:
        end_pattern = r"(?=\Z)"
    pattern = start_pattern + rf"(.*?){end_pattern}"
    match = re.search(pattern, block, re.S | re.M)
    if not match:
        return ""
    return clean_section(f"{match.group(1)}{match.group(2)}")


def parse_case_block(block: str) -> dict[str, str]:
    case_match = CASE_RE.search(block)
    if not case_match:
        raise ValueError("Could not find case id")

    decision = extract_section(block, "决定项", ["加分项", "模拟候选人回答", "备注"])
    bonus = extract_section(block, "加分项", ["模拟候选人回答", "备注"])

    answer = extract_section(block, "模拟候选人回答", ["备注"])
    note = extract_section(block, "备注", [])

    return {
        "case_id": case_match.group(1),
        "决定项": decision,
        "加分项": bonus,
        "模拟回答": answer,
        "备注": note,
    }


def parse_sample_file(path: Path) -> list[dict[str, str]]:
    text = normalize_text(path.read_text(encoding="utf-8"))
    tester = extract_single_line(text, "测试人")
    question = extract_question(text)

    blocks = CASE_RE.split(text)
    if len(blocks) < 3:
        raise ValueError(f"No case blocks found in {path}")

    rows: list[dict[str, str]] = []
    for index in range(1, len(blocks), 2):
        case_id = blocks[index]
        block = f"样本测试序号 {case_id}{blocks[index + 1]}"
        row = parse_case_block(block)
        row["sample_file"] = path.name
        row["tester"] = tester
        row["question"] = question
        rows.append(row)

    if len(rows) != 5:
        raise ValueError(f"Expected 5 case blocks in {path}, found {len(rows)}")

    return rows


def markdown_cell(text: str) -> str:
    if not text:
        return ""
    collapsed = re.sub(r"\n{3,}", "\n\n", text.strip())
    return collapsed.replace("|", r"\|").replace("\n", "<br>")


def sort_key(row: dict[str, str]) -> tuple[int, int]:
    sample_num = int(re.search(r"Sample(\d+)", row["sample_file"]).group(1))
    case_num = int(row["case_id"].split("-")[1])
    return sample_num, case_num


def build_markdown(rows: list[dict[str, str]]) -> str:
    headers = ["case_id", "决定项", "加分项", "模拟回答", "备注"]
    lines = [
        "# Concept Sample Data",
        "",
        f"Generated from `{SOURCE_DIR.relative_to(REPO_ROOT)}`.",
    ]

    grouped_rows: dict[str, list[dict[str, str]]] = {}
    for row in sorted(rows, key=sort_key):
        grouped_rows.setdefault(row["sample_file"], []).append(row)

    for sample_file, sample_rows in grouped_rows.items():
        first_row = sample_rows[0]
        lines.extend(
            [
                "",
                f"## {sample_file}",
                "",
                f"- tester: {first_row['tester']}",
                f"- question: {first_row['question']}",
                "",
                "| " + " | ".join(headers) + " |",
                "| " + " | ".join(["---"] * len(headers)) + " |",
            ]
        )

        for row in sample_rows:
            values = [markdown_cell(row.get(header, "")) for header in headers]
            lines.append("| " + " | ".join(values) + " |")

    lines.append("")
    return "\n".join(lines)


def main() -> None:
    sample_paths = sorted(SOURCE_DIR.glob("FullStack_Sample*.md"))
    if not sample_paths:
        raise FileNotFoundError(f"No sample markdown files found in {SOURCE_DIR}")

    rows: list[dict[str, str]] = []
    for path in sample_paths:
        rows.extend(parse_sample_file(path))

    if len(rows) != 25:
        raise ValueError(f"Expected 25 rows total, found {len(rows)}")

    OUTPUT_PATH.write_text(build_markdown(rows), encoding="utf-8")
    print(f"Wrote {len(rows)} rows to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
