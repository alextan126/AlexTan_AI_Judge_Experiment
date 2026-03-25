"""
Batch Runner: 对同一样本运行 N 轮测试，每轮生成一条 record。
用法:
    python run_batch.py              # 默认 50 轮
    python run_batch.py -n 10        # 10 轮
    python run_batch.py -n 50 -p 9877
"""
import argparse
import copy
import os
import sys
import json
import time
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config import PROJECT_ROOT, MAS_API_URL, CALLBACK_TIMEOUT_SECONDS, CALLBACK_PORT
from callback_server import CallbackServer

import requests as http_requests

SOURCE_DATA_DIR = os.path.join(PROJECT_ROOT, "SourceData")
RECORD_DIR = os.path.join(PROJECT_ROOT, "Report", "Record")
SAMPLE_FILE = os.path.join(PROJECT_ROOT, "Samples", "FullStack_Sample1.md")

QUESTION_TYPES = ("concept", "application", "code")


def load_sample_request() -> dict:
    with open(SAMPLE_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def build_record(items: list, request_id: str, timestamp: str, round_idx: int) -> dict:
    record = {
        "request_id": request_id,
        "round": round_idx,
        "timestamp": timestamp,
        "items": [],
    }
    for item in items:
        item_record = {
            "item_index": item.get("item_index"),
            "ability": item.get("ability"),
            "types": {},
        }
        for q_type in QUESTION_TYPES:
            block = item.get(q_type)
            if block is None:
                item_record["types"][q_type] = None
                continue
            dp = block.get("decision_points", [])
            ep = block.get("extra_points", [])
            item_record["types"][q_type] = {
                "passed": block.get("passed"),
                "decision_points": [{"name": p["name"], "result": p["result"]} for p in dp],
                "extra_points": [{"name": p["name"], "result": p["result"]} for p in ep],
                "decision_results": [p["result"] for p in dp],
                "extra_results": [p["result"] for p in ep],
            }
        record["items"].append(item_record)
    return record


def run_single(server: CallbackServer, template: dict, round_idx: int) -> dict | None:
    """发送一轮请求并等待回调，返回 record dict 或 None。"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    request_id = f"batch_r{round_idx:03d}_{timestamp}"

    request_body = copy.deepcopy(template)
    request_body["business_id"] = request_id
    request_body["callback"] = server.callback_url(request_id)

    try:
        resp = http_requests.post(MAS_API_URL, json=request_body, timeout=30)
        if resp.status_code != 200:
            print(f"HTTP {resp.status_code}")
            return None
    except Exception as e:
        print(f"请求失败: {e}")
        return None

    result = server.wait_for_result(request_id, timeout=CALLBACK_TIMEOUT_SECONDS)
    if result is None:
        print("超时")
        return None

    items = result.get("data", {}).get("data", {}).get("items", [])
    if not items:
        print("无 items")
        return None

    cb_path = os.path.join(SOURCE_DATA_DIR, f"{request_id}_callback.json")
    with open(cb_path, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    return build_record(items, request_id, timestamp, round_idx)


def main():
    parser = argparse.ArgumentParser(description="MAS Judger 批量测试")
    parser.add_argument("-n", "--rounds", type=int, default=50, help="测试轮数 (默认 50)")
    parser.add_argument("-p", "--port", type=int, default=CALLBACK_PORT, help="回调端口")
    args = parser.parse_args()

    os.makedirs(SOURCE_DATA_DIR, exist_ok=True)
    os.makedirs(RECORD_DIR, exist_ok=True)

    print(f"[启动] 加载样本: {SAMPLE_FILE}")
    template = load_sample_request()
    print(f"[启动] 计划运行 {args.rounds} 轮\n")

    server = CallbackServer(port=args.port)
    server.start()
    print(f"[启动] 回调服务器: {server.base_url}\n")

    success, fail = 0, 0

    try:
        for r in range(1, args.rounds + 1):
            print(f"  [{r}/{args.rounds}] 发送...", end=" ", flush=True)
            t0 = time.time()

            record = run_single(server, template, r)

            elapsed = time.time() - t0
            if record is None:
                fail += 1
                print(f"FAIL ({elapsed:.1f}s)")
                continue

            record_path = os.path.join(RECORD_DIR, f"record_r{r:03d}.json")
            with open(record_path, "w", encoding="utf-8") as f:
                json.dump(record, f, ensure_ascii=False, indent=2)

            types_summary = []
            for item in record["items"]:
                for qt in QUESTION_TYPES:
                    tb = item["types"].get(qt)
                    if tb:
                        dp = tb["decision_results"]
                        ep = tb["extra_results"]
                        types_summary.append(f"{qt}:dp={dp} ep={ep}")
            summary_str = "  ".join(types_summary)

            success += 1
            print(f"OK ({elapsed:.1f}s)  {summary_str}")

    except KeyboardInterrupt:
        print("\n\n[中断] 用户取消")
    finally:
        server.stop()

    print(f"\n{'=' * 50}")
    print(f"  完成: {success} 成功, {fail} 失败, 共 {success + fail}/{args.rounds} 轮")
    print(f"  Record 目录: {RECORD_DIR}")
    print(f"{'=' * 50}")


if __name__ == "__main__":
    main()
