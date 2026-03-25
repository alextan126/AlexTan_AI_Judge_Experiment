import sys
import os
from typing import List, Dict, Any, Tuple

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "RelatedAlgorithm"))
from gini_impurity import gini_impurity

from config import QUESTION_TYPES


def _extract_points(
    item: Dict[str, Any], q_type: str
) -> Tuple[List[Dict], List[Dict]]:
    """从一个 item 的某题型中提取 decision_points 和 extra_points。"""
    block = item.get(q_type)
    if block is None:
        return [], []
    return block.get("decision_points", []), block.get("extra_points", [])


def _match_points(
    sys_points: List[Dict], gt_points: List[Dict]
) -> Tuple[int, int]:
    """按 name 匹配判定点，返回 (匹配数, 总数)。以 GT 为基准。"""
    sys_map = {p["name"]: p["result"] for p in sys_points}
    matched = 0
    for gt_p in gt_points:
        if sys_map.get(gt_p["name"]) == gt_p["result"]:
            matched += 1
    return matched, len(gt_points)


def compute_single_round_metrics(
    sys_items: List[Dict[str, Any]],
    gt_items: List[Dict[str, Any]],
) -> Dict[str, Any]:
    """
    对比一轮系统输出与 Ground Truth，计算四项准确率指标 + 短路合规率。

    返回:
        {
            "overall_accuracy": float,
            "decision_accuracy": float,
            "extra_accuracy": float,
            "short_circuit_compliance": float,
            "details": [...]   # 逐题型详细结果
        }
    """
    gt_map = {item["item_index"]: item for item in gt_items}

    total_all_match, total_all_count = 0, 0
    total_dec_match, total_dec_count = 0, 0
    total_ext_match, total_ext_count = 0, 0
    sc_applicable, sc_compliant = 0, 0

    details = []

    for sys_item in sys_items:
        idx = sys_item["item_index"]
        gt_item = gt_map.get(idx)
        if gt_item is None:
            continue

        item_detail = {"item_index": idx, "types": {}}

        for q_type in QUESTION_TYPES:
            sys_dp, sys_ep = _extract_points(sys_item, q_type)
            gt_dp, gt_ep = _extract_points(gt_item, q_type)

            if not gt_dp and not gt_ep:
                continue

            dec_m, dec_t = _match_points(sys_dp, gt_dp)
            ext_m, ext_t = _match_points(sys_ep, gt_ep)

            total_dec_match += dec_m
            total_dec_count += dec_t
            total_ext_match += ext_m
            total_ext_count += ext_t
            total_all_match += dec_m + ext_m
            total_all_count += dec_t + ext_t

            gt_block = gt_item.get(q_type, {})
            gt_passed = gt_block.get("passed", True) if gt_block else True
            if not gt_passed:
                sc_applicable += 1
                sys_block = sys_item.get(q_type, {})
                sys_ep_list = sys_block.get("extra_points", []) if sys_block else []
                if len(sys_ep_list) == 0:
                    sc_compliant += 1

            item_detail["types"][q_type] = {
                "decision_match": dec_m,
                "decision_total": dec_t,
                "extra_match": ext_m,
                "extra_total": ext_t,
            }

        details.append(item_detail)

    return {
        "overall_accuracy": total_all_match / total_all_count if total_all_count else 0.0,
        "decision_accuracy": total_dec_match / total_dec_count if total_dec_count else 0.0,
        "extra_accuracy": total_ext_match / total_ext_count if total_ext_count else 0.0,
        "short_circuit_compliance": sc_compliant / sc_applicable if sc_applicable else 1.0,
        "details": details,
    }


def compute_stability(
    multi_round_results: List[List[Dict[str, Any]]],
    gt_items: List[Dict[str, Any]],
) -> Dict[str, Any]:
    """
    对 N 轮系统输出计算每个判定点的 Gini Impurity，衡量稳定性。

    multi_round_results: 长度为 N 的列表，每个元素是该轮的 sys_items。
    返回:
        {
            "per_point_gini": { "concept.define": 0.0, ... },
            "average_gini": float,
        }
    """
    point_sequences: Dict[str, List[int]] = {}

    gt_map = {item["item_index"]: item for item in gt_items}

    for round_items in multi_round_results:
        sys_map = {item["item_index"]: item for item in round_items}

        for idx, gt_item in gt_map.items():
            sys_item = sys_map.get(idx, {})
            for q_type in QUESTION_TYPES:
                gt_block = gt_item.get(q_type)
                if gt_block is None:
                    continue
                sys_block = sys_item.get(q_type) if sys_item else None

                for point_list_key in ("decision_points", "extra_points"):
                    for gt_p in gt_block.get(point_list_key, []):
                        key = f"item{idx}.{q_type}.{gt_p['name']}"
                        if sys_block:
                            sys_pts = {p["name"]: p["result"] for p in sys_block.get(point_list_key, [])}
                            result = sys_pts.get(gt_p["name"], -1)
                        else:
                            result = -1
                        point_sequences.setdefault(key, []).append(result)

    per_point_gini = {}
    for key, seq in point_sequences.items():
        labels = [str(v) for v in seq]
        per_point_gini[key] = gini_impurity(labels)

    avg = sum(per_point_gini.values()) / len(per_point_gini) if per_point_gini else 0.0

    return {
        "per_point_gini": per_point_gini,
        "average_gini": avg,
    }


def aggregate_multi_round(
    round_metrics: List[Dict[str, Any]],
) -> Dict[str, float]:
    """将多轮的 metrics 取平均。"""
    keys = ["overall_accuracy", "decision_accuracy", "extra_accuracy", "short_circuit_compliance"]
    n = len(round_metrics)
    if n == 0:
        return {k: 0.0 for k in keys}
    return {k: sum(m[k] for m in round_metrics) / n for k in keys}
