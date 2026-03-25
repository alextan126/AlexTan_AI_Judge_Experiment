from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Any


BASE_DIR = Path(__file__).resolve().parent
REPO_ROOT = BASE_DIR.parents[1]
DEFAULT_GT_PATH = BASE_DIR / "concept_ground_truth.json"
DEFAULT_REPORT_ROOT = BASE_DIR / "reports"

TEST_PROGRAM_DIR = REPO_ROOT / "JudgerTesting" / "TestProgram"
if str(TEST_PROGRAM_DIR) not in sys.path:
    sys.path.insert(0, str(TEST_PROGRAM_DIR))

from metrics import aggregate_multi_round, compute_single_round_metrics, compute_stability  # noqa: E402

from concept_multiagent_judger import JudgerError, judge_concept_answer  # noqa: E402


POINT_ORDER = [
    ("decision_points", "define"),
    ("extra_points", "keyword"),
    ("extra_points", "keyword_first_sentence"),
    ("extra_points", "keyword_no_repeat"),
    ("extra_points", "not_overtime"),
    ("extra_points", "define_first_sentence"),
    ("extra_points", "order_define_explain"),
]


def _load_ground_truth(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise FileNotFoundError(
            f"Ground-truth JSON not found at {path}. Run sample_data_to_ground_truth_json.py first."
        )
    return json.loads(path.read_text(encoding="utf-8"))


def _point_map(block: dict[str, Any], key: str) -> dict[str, int]:
    return {point["name"]: int(point["result"]) for point in block.get(key, [])}


def _build_record(round_index: int, sys_items: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "round_index": round_index,
        "generated_at": datetime.now().isoformat(),
        "items": [
            {
                "item_index": item["item_index"],
                "sample_file": item.get("sample_file"),
                "case_id": item.get("case_id"),
                "types": {"concept": item["concept"]},
            }
            for item in sys_items
        ],
    }


def _build_mismatches(
    sys_items: list[dict[str, Any]],
    gt_items: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    gt_map = {item["item_index"]: item for item in gt_items}
    mismatches: list[dict[str, Any]] = []

    for sys_item in sys_items:
        gt_item = gt_map[sys_item["item_index"]]
        sys_block = sys_item.get("concept", {})
        gt_block = gt_item.get("concept", {})

        point_mismatches: list[dict[str, Any]] = []
        for list_name, point_name in POINT_ORDER:
            sys_value = _point_map(sys_block, list_name).get(point_name)
            gt_value = _point_map(gt_block, list_name).get(point_name)
            if sys_value != gt_value:
                point_mismatches.append(
                    {
                        "point_name": point_name,
                        "expected": gt_value,
                        "actual": sys_value,
                    }
                )

        sys_passed = bool(sys_block.get("passed", False))
        gt_passed = bool(gt_block.get("passed", False))
        if sys_passed != gt_passed:
            point_mismatches.append(
                {
                    "point_name": "passed",
                    "expected": gt_passed,
                    "actual": sys_passed,
                }
            )

        if point_mismatches:
            mismatches.append(
                {
                    "item_index": sys_item["item_index"],
                    "sample_file": gt_item.get("sample_file"),
                    "case_id": gt_item.get("case_id"),
                    "question": gt_item.get("question"),
                    "simulated_answer": gt_item.get("simulated_answer"),
                    "point_mismatches": point_mismatches,
                    "human_notes": gt_item.get("notes", ""),
                    "ai_extracted_definition": sys_block.get("extracted_definition", ""),
                }
            )

    return mismatches


def _build_point_accuracy(
    sys_items: list[dict[str, Any]],
    gt_items: list[dict[str, Any]],
) -> dict[str, dict[str, float]]:
    gt_map = {item["item_index"]: item for item in gt_items}
    summary: dict[str, dict[str, float]] = {}

    for list_name, point_name in POINT_ORDER:
        matched = 0
        total = 0
        for sys_item in sys_items:
            gt_item = gt_map[sys_item["item_index"]]
            sys_value = _point_map(sys_item.get("concept", {}), list_name).get(point_name, -1)
            gt_value = _point_map(gt_item.get("concept", {}), list_name).get(point_name, -1)
            if gt_value == -1:
                continue
            total += 1
            if sys_value == gt_value:
                matched += 1

        summary[point_name] = {
            "matched": matched,
            "total": total,
            "accuracy": matched / total if total else 0.0,
        }

    return summary


def run_eval(
    *,
    ground_truth_path: Path,
    output_dir: Path,
    rounds: int,
    max_items: int | None,
) -> dict[str, Any]:
    gt_payload = _load_ground_truth(ground_truth_path)
    gt_items = gt_payload["items"]
    if max_items is not None:
        gt_items = gt_items[:max_items]

    if not gt_items:
        raise ValueError("No concept items available for evaluation.")

    output_dir.mkdir(parents=True, exist_ok=True)

    round_metrics: list[dict[str, Any]] = []
    multi_round_sys_items: list[list[dict[str, Any]]] = []
    per_round_summary: list[dict[str, Any]] = []

    for round_index in range(1, rounds + 1):
        sys_items: list[dict[str, Any]] = []
        for gt_item in gt_items:
            sys_items.append(
                judge_concept_answer(
                    question=gt_item["question"],
                    user_answer=gt_item["simulated_answer"],
                    item_index=gt_item["item_index"],
                    ability=gt_item.get("ability"),
                    sample_file=gt_item.get("sample_file"),
                    case_id=gt_item.get("case_id"),
                )
            )

        metrics = compute_single_round_metrics(sys_items, gt_items)
        mismatches = _build_mismatches(sys_items, gt_items)
        point_accuracy = _build_point_accuracy(sys_items, gt_items)

        round_metrics.append(metrics)
        multi_round_sys_items.append(sys_items)
        per_round_summary.append(
            {
                "round_index": round_index,
                "metrics": {key: value for key, value in metrics.items() if key != "details"},
                "mismatch_count": len(mismatches),
                "point_accuracy": point_accuracy,
            }
        )

        (output_dir / f"round_{round_index:02d}_ai_items.json").write_text(
            json.dumps(sys_items, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        (output_dir / f"round_{round_index:02d}_record.json").write_text(
            json.dumps(_build_record(round_index, sys_items), ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        (output_dir / f"round_{round_index:02d}_mismatches.json").write_text(
            json.dumps(mismatches, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )

    aggregated = aggregate_multi_round(round_metrics)
    stability = compute_stability(multi_round_sys_items, gt_items)
    summary = {
        "generated_at": datetime.now().isoformat(),
        "ground_truth_path": str(ground_truth_path),
        "total_items": len(gt_items),
        "rounds": rounds,
        "aggregated": aggregated,
        "stability": stability,
        "per_round": per_round_summary,
    }

    (output_dir / "summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    return summary


def main() -> None:
    parser = argparse.ArgumentParser(description="Run concept multi-agent evaluation against human labels")
    parser.add_argument("--ground-truth", default=str(DEFAULT_GT_PATH), help="Ground-truth JSON path")
    parser.add_argument("--output-dir", help="Directory to store run artifacts")
    parser.add_argument("--rounds", type=int, default=1, help="How many times to evaluate all items")
    parser.add_argument("--max-items", type=int, help="Optional limit for debugging")
    args = parser.parse_args()

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir = Path(args.output_dir) if args.output_dir else DEFAULT_REPORT_ROOT / f"concept_eval_{timestamp}"

    summary = run_eval(
        ground_truth_path=Path(args.ground_truth),
        output_dir=output_dir,
        rounds=args.rounds,
        max_items=args.max_items,
    )

    aggregated = summary["aggregated"]
    print(f"[done] Results saved to {output_dir}")
    print(f"  overall_accuracy: {aggregated['overall_accuracy']:.3f}")
    print(f"  decision_accuracy: {aggregated['decision_accuracy']:.3f}")
    print(f"  extra_accuracy: {aggregated['extra_accuracy']:.3f}")
    print(f"  short_circuit_compliance: {aggregated['short_circuit_compliance']:.3f}")


if __name__ == "__main__":
    try:
        main()
    except (JudgerError, FileNotFoundError, ValueError) as exc:
        raise SystemExit(f"[error] {exc}")
