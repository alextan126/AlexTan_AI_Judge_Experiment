"""
Metrics Calculator: 读取 Report/Record/ 下的所有 record，
对照 Ground Truth 计算 5 项指标，输出报告到 Report/。

用法:
    python calc_metrics.py
    python calc_metrics.py --gt ../Samples/FullStack_Sample1_gt.json
"""
import argparse
import os
import sys
import json
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "RelatedAlgorithm"))

from config import PROJECT_ROOT
from gini_impurity import gini_impurity

RECORD_DIR = os.path.join(PROJECT_ROOT, "Report", "Record")
REPORT_DIR = os.path.join(PROJECT_ROOT, "Report")
DEFAULT_GT = os.path.join(PROJECT_ROOT, "Samples", "FullStack_Sample1_gt.json")
QUESTION_TYPES = ("concept", "application", "code")


def load_gt(path: str) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def load_records(directory: str) -> list:
    records = []
    for fn in sorted(os.listdir(directory)):
        if fn.endswith("_record.json") or fn.startswith("record_"):
            fp = os.path.join(directory, fn)
            with open(fp, "r", encoding="utf-8") as f:
                records.append(json.load(f))
    return records


def match_points(sys_points: list, gt_points: list) -> tuple:
    """按 name 匹配，返回 (match_count, total_count)。"""
    sys_map = {p["name"]: p["result"] for p in sys_points}
    matched = 0
    for gp in gt_points:
        if sys_map.get(gp["name"]) == gp["result"]:
            matched += 1
    return matched, len(gt_points)


def calc_single_round(record: dict, gt_items: list) -> dict:
    """计算单轮的 4 项准确率 + 短路合规率。"""
    gt_map = {it["item_index"]: it for it in gt_items}

    dec_match, dec_total = 0, 0
    ext_match, ext_total = 0, 0
    sc_applicable, sc_compliant = 0, 0

    for rec_item in record["items"]:
        idx = rec_item["item_index"]
        gt_item = gt_map.get(idx)
        if gt_item is None:
            continue

        for qt in QUESTION_TYPES:
            sys_block = rec_item["types"].get(qt)
            gt_block = gt_item.get(qt)
            if gt_block is None:
                continue

            gt_dp = gt_block.get("decision_points", [])
            gt_ep = gt_block.get("extra_points", [])
            sys_dp = sys_block.get("decision_points", []) if sys_block else []
            sys_ep = sys_block.get("extra_points", []) if sys_block else []

            dm, dt = match_points(sys_dp, gt_dp)
            em, et = match_points(sys_ep, gt_ep)
            dec_match += dm
            dec_total += dt
            ext_match += em
            ext_total += et

            gt_passed = gt_block.get("passed", True)
            if not gt_passed:
                sc_applicable += 1
                if sys_block and len(sys_block.get("extra_points", [])) == 0:
                    sc_compliant += 1

    all_match = dec_match + ext_match
    all_total = dec_total + ext_total

    return {
        "overall_accuracy": all_match / all_total if all_total else 0.0,
        "decision_accuracy": dec_match / dec_total if dec_total else 0.0,
        "extra_accuracy": ext_match / ext_total if ext_total else 0.0,
        "short_circuit_compliance": sc_compliant / sc_applicable if sc_applicable else 1.0,
    }


def calc_stability(records: list, gt_items: list) -> dict:
    """对 N 轮 record 计算每个判定点的 Gini Impurity。"""
    gt_map = {it["item_index"]: it for it in gt_items}
    point_sequences: dict = {}

    for record in records:
        rec_map = {it["item_index"]: it for it in record["items"]}
        for idx, gt_item in gt_map.items():
            rec_item = rec_map.get(idx, {"types": {}})
            for qt in QUESTION_TYPES:
                gt_block = gt_item.get(qt)
                if gt_block is None:
                    continue
                sys_block = rec_item["types"].get(qt)

                for key_list in ("decision_points", "extra_points"):
                    for gp in gt_block.get(key_list, []):
                        point_key = f"{qt}.{gp['name']}"
                        if sys_block:
                            sys_pts = {p["name"]: p["result"] for p in sys_block.get(key_list, [])}
                            val = sys_pts.get(gp["name"], -1)
                        else:
                            val = -1
                        point_sequences.setdefault(point_key, []).append(val)

    per_point_gini = {}
    for key, seq in point_sequences.items():
        per_point_gini[key] = gini_impurity([str(v) for v in seq])

    avg_gini = sum(per_point_gini.values()) / len(per_point_gini) if per_point_gini else 0.0
    return {"per_point_gini": per_point_gini, "average_gini": avg_gini}


def fmt_pct(v: float) -> str:
    return f"{v * 100:.2f}%"


def main():
    parser = argparse.ArgumentParser(description="计算 Judger 测试 Metrics")
    parser.add_argument("--gt", default=DEFAULT_GT, help="Ground Truth 文件路径")
    parser.add_argument("--record-dir", default=RECORD_DIR, help="Record 目录")
    args = parser.parse_args()

    gt_data = load_gt(args.gt)
    gt_items = gt_data["items"]
    print(f"[加载] Ground Truth: {args.gt}")
    print(f"       样本: {gt_data.get('sample_id', '?')} - {gt_data.get('description', '')}")

    records = load_records(args.record_dir)
    print(f"[加载] Records: {len(records)} 轮  ({args.record_dir})\n")

    if not records:
        print("[错误] 没有找到 record 文件，请先运行 run_batch.py")
        sys.exit(1)

    # --- 逐轮 metrics ---
    round_metrics = []
    for i, rec in enumerate(records):
        rm = calc_single_round(rec, gt_items)
        round_metrics.append(rm)

    # --- 汇总 ---
    n = len(round_metrics)
    keys = ["overall_accuracy", "decision_accuracy", "extra_accuracy", "short_circuit_compliance"]
    aggregated = {k: sum(m[k] for m in round_metrics) / n for k in keys}

    # --- 稳定性 ---
    stability = calc_stability(records, gt_items)

    # === 输出 ===
    sep = "=" * 60
    print(sep)
    print(f"  MAS Judger 质量测试报告  ({n} 轮)")
    print(sep)

    print(f"\n  {'指标':<20} {'值':>10}")
    print(f"  {'-' * 35}")
    print(f"  {'整体准确率':<18} {fmt_pct(aggregated['overall_accuracy']):>10}")
    print(f"  {'决定项准确率':<17} {fmt_pct(aggregated['decision_accuracy']):>10}")
    print(f"  {'加分项准确率':<17} {fmt_pct(aggregated['extra_accuracy']):>10}")
    print(f"  {'短路合规率':<18} {fmt_pct(aggregated['short_circuit_compliance']):>10}")
    print(f"  {'判定稳定性(avg G)':<16} {stability['average_gini']:>10.4f}")

    print(f"\n  --- 逐判定点 Gini Impurity ---")
    for key, g in sorted(stability["per_point_gini"].items()):
        tag = "稳定" if g == 0.0 else f"波动"
        print(f"  {key:<35} {g:.4f}  [{tag}]")

    print(f"\n  --- 逐轮准确率 ---")
    for i, rm in enumerate(round_metrics):
        print(f"  第{i+1:>3}轮: 整体={fmt_pct(rm['overall_accuracy'])}  "
              f"决定={fmt_pct(rm['decision_accuracy'])}  "
              f"加分={fmt_pct(rm['extra_accuracy'])}  "
              f"短路={fmt_pct(rm['short_circuit_compliance'])}")

    print(sep)

    # --- 保存 JSON 报告 ---
    report = {
        "generated_at": datetime.now().isoformat(),
        "ground_truth": args.gt,
        "total_rounds": n,
        "aggregated": aggregated,
        "stability": stability,
        "per_round": round_metrics,
    }
    os.makedirs(REPORT_DIR, exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_path = os.path.join(REPORT_DIR, f"metrics_report_{ts}.json")
    with open(report_path, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    print(f"\n[保存] 报告 -> {report_path}")


if __name__ == "__main__":
    main()
