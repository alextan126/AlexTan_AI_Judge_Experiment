import argparse
import concurrent.futures
import json
import time
from datetime import datetime
from pathlib import Path

from app_mixed_agent_judge import judge_app_answer_mixed
from app_single_agent_judger import judge_app_answer_single

BASE_DIR = Path(__file__).resolve().parents[2]
APP_DIR = BASE_DIR / "AlternativeSolution" / "应用题"
GROUND_TRUTH_FILE = APP_DIR / "app_ground_truth.json"
REPORTS_DIR = APP_DIR / "reports"


def _run_single(question: str, answer: str, correct_answer: str) -> dict:
    start_time = time.time()
    result = judge_app_answer_single(question, answer, correct_answer)
    result["elapsed_seconds"] = round(time.time() - start_time, 2)
    return result


def _run_mixed(question: str, answer: str, correct_answer: str) -> dict:
    start_time = time.time()
    result = judge_app_answer_mixed(question, answer, correct_answer)
    result["elapsed_seconds"] = round(time.time() - start_time, 2)
    return result


def _evaluate_one(question: str, answer: str, correct_answer: str, judger: str) -> dict:
    if judger == "single":
        return {"single": _run_single(question, answer, correct_answer)}
    if judger == "mixed":
        return {"mixed": _run_mixed(question, answer, correct_answer)}

    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
        single_future = executor.submit(_run_single, question, answer, correct_answer)
        mixed_future = executor.submit(_run_mixed, question, answer, correct_answer)
        return {
            "single": single_future.result(),
            "mixed": mixed_future.result(),
        }


def _match_block(gt: dict, ai_result: dict) -> dict:
    ai_level = ai_result.get("stare_level", "")
    ai_score = ai_result.get("score", 0)
    gt_level = gt["stare_level"]
    gt_score = gt["score"]
    return {
        "stare_level": ai_level,
        "score": ai_score,
        "reasoning": ai_result.get("reasoning", ""),
        "components": ai_result.get("components", {}),
        "elapsed_seconds": ai_result.get("elapsed_seconds", 0),
        "level_match": ai_level == gt_level,
        "score_match": ai_score == gt_score,
    }


def _empty_stats() -> dict:
    return {
        "level_correct": 0,
        "score_correct": 0,
        "mismatch_count": 0,
    }


def _finalize_stats(stats: dict, total: int) -> dict:
    return {
        "level_correct": stats["level_correct"],
        "score_correct": stats["score_correct"],
        "mismatch_count": stats["mismatch_count"],
        "accuracy_level": round(stats["level_correct"] / total, 4) if total else 0,
        "accuracy_score": round(stats["score_correct"] / total, 4) if total else 0,
    }


def main():
    parser = argparse.ArgumentParser(description="Run Application Question Evaluation")
    parser.add_argument(
        "--judger",
        choices=["single", "mixed", "both"],
        default="both",
        help="Choose single, mixed, or both judger architectures",
    )
    args = parser.parse_args()

    if not GROUND_TRUTH_FILE.exists():
        print(f"Ground truth file not found: {GROUND_TRUTH_FILE}")
        return

    with open(GROUND_TRUTH_FILE, "r", encoding="utf-8") as f:
        ground_truth = json.load(f)

    print(f"Loaded {len(ground_truth)} samples from ground truth.")
    print(f"Using judger mode: {args.judger}")

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_dir = REPORTS_DIR / f"app_eval_{args.judger}_{timestamp}"
    report_dir.mkdir(parents=True, exist_ok=True)

    ai_items = []
    mismatches = []
    single_stats = _empty_stats()
    mixed_stats = _empty_stats()

    for i, gt in enumerate(ground_truth, start=1):
        print(f"Processing sample {i}/{len(ground_truth)}: {gt['file_name']} - {gt['case_id']}")
        question = gt["question"]
        answer = gt["simulated_answer"]
        correct_answer = gt.get("correct_answer", "")

        raw_results = _evaluate_one(question, answer, correct_answer, args.judger)

        item = {
            "file_name": gt["file_name"],
            "case_id": gt["case_id"],
            "question": question,
            "correct_answer": correct_answer,
            "simulated_answer": answer,
            "ground_truth": {
                "stare_level": gt["stare_level"],
                "score": gt["score"],
                "notes": gt["notes"],
            },
        }

        if "single" in raw_results:
            single_block = _match_block(gt, raw_results["single"])
            item["single"] = single_block
            if single_block["level_match"]:
                single_stats["level_correct"] += 1
            if single_block["score_match"]:
                single_stats["score_correct"] += 1
            if not single_block["level_match"] or not single_block["score_match"]:
                single_stats["mismatch_count"] += 1

        if "mixed" in raw_results:
            mixed_block = _match_block(gt, raw_results["mixed"])
            item["mixed"] = mixed_block
            if mixed_block["level_match"]:
                mixed_stats["level_correct"] += 1
            if mixed_block["score_match"]:
                mixed_stats["score_correct"] += 1
            if not mixed_block["level_match"] or not mixed_block["score_match"]:
                mixed_stats["mismatch_count"] += 1

        ai_items.append(item)

        single_mismatch = "single" in item and (
            not item["single"]["level_match"] or not item["single"]["score_match"]
        )
        mixed_mismatch = "mixed" in item and (
            not item["mixed"]["level_match"] or not item["mixed"]["score_match"]
        )
        if single_mismatch or mixed_mismatch:
            mismatch_item = {
                "file_name": gt["file_name"],
                "case_id": gt["case_id"],
                "ground_truth": item["ground_truth"],
            }
            if "single" in item:
                mismatch_item["single"] = item["single"]
            if "mixed" in item:
                mismatch_item["mixed"] = item["mixed"]
            mismatches.append(mismatch_item)

    total = len(ground_truth)
    summary = {
        "judger_mode": args.judger,
        "total_samples": total,
    }
    if args.judger in {"single", "both"}:
        summary["single"] = _finalize_stats(single_stats, total)
    if args.judger in {"mixed", "both"}:
        summary["mixed"] = _finalize_stats(mixed_stats, total)

    with open(report_dir / "ai_items.json", "w", encoding="utf-8") as f:
        json.dump(ai_items, f, ensure_ascii=False, indent=2)

    with open(report_dir / "mismatches.json", "w", encoding="utf-8") as f:
        json.dump(mismatches, f, ensure_ascii=False, indent=2)

    with open(report_dir / "summary.json", "w", encoding="utf-8") as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)

    print("\nEvaluation Complete!")
    if "single" in summary:
        print(
            "Single Agent - "
            f"Level Accuracy: {summary['single']['accuracy_level']:.2%}, "
            f"Score Accuracy: {summary['single']['accuracy_score']:.2%}"
        )
    if "mixed" in summary:
        print(
            "Mixed Agent  - "
            f"Level Accuracy: {summary['mixed']['accuracy_level']:.2%}, "
            f"Score Accuracy: {summary['mixed']['accuracy_score']:.2%}"
        )
    print(f"Reports saved to: {report_dir}")


if __name__ == "__main__":
    main()
