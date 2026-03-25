import argparse
import sys

from config import TEST_ROUNDS, CALLBACK_PORT
from sample_loader import load_all_samples, validate_sample
from callback_server import CallbackServer
from api_client import send_review_request
from metrics import compute_single_round_metrics, compute_stability, aggregate_multi_round
from report import (
    print_sample_report,
    print_global_summary,
    save_report,
    build_report_data,
)


def _extract_sys_items(callback_data: dict) -> list:
    """从回调 JSON 中提取 data.data.items 列表。"""
    return callback_data.get("data", {}).get("data", {}).get("items", [])


def run_test(rounds: int, port: int):
    print(f"[启动] 加载样本...")
    samples = load_all_samples()
    print(f"[启动] 共加载 {len(samples)} 个样本")

    for s in samples:
        errors = validate_sample(s)
        if errors:
            print(f"[警告] 样本 {s.get('sample_id', '?')} 格式错误: {errors}")
            sys.exit(1)

    server = CallbackServer(port=port)
    server.start()
    print(f"[启动] 回调服务器已启动: {server.base_url}")

    all_sample_reports = []

    try:
        for sample in samples:
            sid = sample["sample_id"]
            gt_items = sample["ground_truth"]["items"]
            print(f"\n{'─' * 50}")
            print(f"[测试] 样本: {sid}  ({rounds} 轮)")

            round_metrics_list = []
            multi_round_sys_items = []

            for r in range(1, rounds + 1):
                request_id = f"{sid}_round{r}"
                callback_url = server.callback_url(request_id)

                print(f"  第 {r}/{rounds} 轮: 发送请求...", end=" ", flush=True)
                api_resp = send_review_request(sample, callback_url, r)

                if api_resp and api_resp.get("error"):
                    print(f"请求失败: {api_resp['error']}")
                    round_metrics_list.append(_empty_metrics())
                    multi_round_sys_items.append([])
                    continue

                print("等待回调...", end=" ", flush=True)
                result = server.wait_for_result(request_id)

                if result is None:
                    print("超时!")
                    round_metrics_list.append(_empty_metrics())
                    multi_round_sys_items.append([])
                    continue

                sys_items = _extract_sys_items(result)
                multi_round_sys_items.append(sys_items)

                rm = compute_single_round_metrics(sys_items, gt_items)
                round_metrics_list.append(rm)
                print(f"完成 (整体准确率: {rm['overall_accuracy'] * 100:.1f}%)")

            aggregated = aggregate_multi_round(round_metrics_list)
            stability = compute_stability(multi_round_sys_items, gt_items)

            print_sample_report(sid, round_metrics_list, aggregated, stability)

            all_sample_reports.append({
                "sample_id": sid,
                "rounds": [
                    {k: v for k, v in rm.items() if k != "details"}
                    for rm in round_metrics_list
                ],
                "aggregated": aggregated,
                "stability": stability,
            })

    finally:
        server.stop()
        print("\n[完成] 回调服务器已关闭")

    if all_sample_reports:
        keys = ["overall_accuracy", "decision_accuracy", "extra_accuracy", "short_circuit_compliance"]
        n = len(all_sample_reports)
        global_agg = {
            k: sum(sr["aggregated"][k] for sr in all_sample_reports) / n
            for k in keys
        }
        global_avg_gini = sum(
            sr["stability"]["average_gini"] for sr in all_sample_reports
        ) / n

        print_global_summary(global_agg, global_avg_gini)

        report_data = build_report_data(all_sample_reports, global_agg, global_avg_gini, rounds)
        filepath = save_report(report_data)
        print(f"\n[报告] 已保存至: {filepath}")


def _empty_metrics() -> dict:
    return {
        "overall_accuracy": 0.0,
        "decision_accuracy": 0.0,
        "extra_accuracy": 0.0,
        "short_circuit_compliance": 0.0,
        "details": [],
    }


def main():
    parser = argparse.ArgumentParser(description="MAS Judger 质量测试程序")
    parser.add_argument("-n", "--rounds", type=int, default=TEST_ROUNDS, help=f"每样本测试轮数 (默认 {TEST_ROUNDS})")
    parser.add_argument("-p", "--port", type=int, default=CALLBACK_PORT, help=f"回调服务器端口 (默认 {CALLBACK_PORT})")
    args = parser.parse_args()

    run_test(rounds=args.rounds, port=args.port)


if __name__ == "__main__":
    main()
