import json
import os
from datetime import datetime
from typing import Dict, List, Any

from config import REPORTS_DIR


def _fmt_pct(value: float) -> str:
    return f"{value * 100:.2f}%"


def print_sample_report(
    sample_id: str,
    round_metrics: List[Dict[str, Any]],
    aggregated: Dict[str, float],
    stability: Dict[str, Any],
):
    """在控制台输出单个样本的测试报告。"""
    sep = "=" * 60
    print(f"\n{sep}")
    print(f"  样本: {sample_id}")
    print(sep)

    for i, rm in enumerate(round_metrics):
        print(f"  第 {i + 1} 轮:")
        print(f"    整体准确率:     {_fmt_pct(rm['overall_accuracy'])}")
        print(f"    决定项准确率:   {_fmt_pct(rm['decision_accuracy'])}")
        print(f"    加分项准确率:   {_fmt_pct(rm['extra_accuracy'])}")
        print(f"    短路合规率:     {_fmt_pct(rm['short_circuit_compliance'])}")

    print(f"\n  --- N 轮汇总 ---")
    print(f"    平均整体准确率:     {_fmt_pct(aggregated['overall_accuracy'])}")
    print(f"    平均决定项准确率:   {_fmt_pct(aggregated['decision_accuracy'])}")
    print(f"    平均加分项准确率:   {_fmt_pct(aggregated['extra_accuracy'])}")
    print(f"    平均短路合规率:     {_fmt_pct(aggregated['short_circuit_compliance'])}")
    print(f"    判定稳定性 (avg Gini): {stability['average_gini']:.4f}")

    if stability["per_point_gini"]:
        print(f"\n  --- 逐判定点 Gini ---")
        for key, g in sorted(stability["per_point_gini"].items()):
            tag = "稳定" if g == 0.0 else "波动"
            print(f"    {key}: {g:.4f}  [{tag}]")

    print(sep)


def print_global_summary(global_agg: Dict[str, float], global_avg_gini: float):
    """输出所有样本的全局汇总。"""
    sep = "#" * 60
    print(f"\n{sep}")
    print("  全局汇总")
    print(sep)
    print(f"    整体准确率:     {_fmt_pct(global_agg['overall_accuracy'])}")
    print(f"    决定项准确率:   {_fmt_pct(global_agg['decision_accuracy'])}")
    print(f"    加分项准确率:   {_fmt_pct(global_agg['extra_accuracy'])}")
    print(f"    短路合规率:     {_fmt_pct(global_agg['short_circuit_compliance'])}")
    print(f"    平均判定稳定性: {global_avg_gini:.4f}")
    print(sep)


def save_report(report_data: Dict[str, Any]) -> str:
    """将完整报告保存为 JSON 文件，返回文件路径。"""
    os.makedirs(REPORTS_DIR, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filepath = os.path.join(REPORTS_DIR, f"report_{timestamp}.json")
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(report_data, f, ensure_ascii=False, indent=2)
    return filepath


def build_report_data(
    sample_reports: List[Dict[str, Any]],
    global_agg: Dict[str, float],
    global_avg_gini: float,
    test_rounds: int,
) -> Dict[str, Any]:
    """组装完整报告数据结构。"""
    return {
        "generated_at": datetime.now().isoformat(),
        "test_rounds": test_rounds,
        "samples": sample_reports,
        "global_summary": {
            **global_agg,
            "average_gini": global_avg_gini,
        },
    }
