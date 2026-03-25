"""
Smoke Test: 测通 MAS API 调用链路
1. 从 Samples/FullStack_Sample1.md 加载请求样本
2. 启动本地回调服务器
3. 发送一次请求到 MAS API
4. 等待回调结果
5. 将原始 Response 保存到 SourceData/ 文件夹
6. 将概览判断记录保存到 Report/Record/ 文件夹
"""
import os
import sys
import json
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config import PROJECT_ROOT, MAS_API_URL, CALLBACK_TIMEOUT_SECONDS
from callback_server import CallbackServer

import requests as http_requests

SOURCE_DATA_DIR = os.path.join(PROJECT_ROOT, "SourceData")
RECORD_DIR = os.path.join(PROJECT_ROOT, "Report", "解决方案_Record", "1_1")
SAMPLE_FILE = os.path.join(PROJECT_ROOT, "Report", "解决方案_Record", "1_1", "Sample.md")

QUESTION_TYPES = ("concept", "application", "code")


def load_sample_request() -> dict:
    with open(SAMPLE_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def build_record(items: list, request_id: str, timestamp: str) -> dict:
    """从回调结果中提取每个 item 的概览判断记录。"""
    record = {
        "request_id": request_id,
        "timestamp": timestamp,
        "items": [],
    }
    for item in items:
        item_record = {"item_index": item.get("item_index"), "ability": item.get("ability"), "types": {}}
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


def print_record(items: list):
    """在控制台输出概览。"""
    for item in items:
        idx = item.get("item_index", "?")
        print(f"\n       --- item_index={idx} 概览 ---")
        for q_type in QUESTION_TYPES:
            block = item.get(q_type)
            if block:
                passed = block.get("passed")
                dp = [p["result"] for p in block.get("decision_points", [])]
                ep = [p["result"] for p in block.get("extra_points", [])]
                print(f"       {q_type}: passed={passed}  决定项={dp}  加分项={ep}")
            else:
                print(f"       {q_type}: null")


def main():
    os.makedirs(SOURCE_DATA_DIR, exist_ok=True)
    os.makedirs(RECORD_DIR, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    request_id = f"smoke_{timestamp}"

    print("[1/6] 加载请求样本...")
    request_body = load_sample_request()
    print(f"       来源: {SAMPLE_FILE}")
    print(f"       item_num: {request_body['data']['item_num']}")

    request_body["business_id"] = request_id

    print("[2/6] 启动回调服务器...")
    server = CallbackServer()
    server.start()
    callback_url = server.callback_url(request_id)
    request_body["callback"] = callback_url
    print(f"       回调地址: {callback_url}")

    req_path = os.path.join(SOURCE_DATA_DIR, f"{request_id}_request.json")
    with open(req_path, "w", encoding="utf-8") as f:
        json.dump(request_body, f, ensure_ascii=False, indent=2)
    print(f"       已保存请求体 -> {req_path}")

    print(f"[3/6] POST -> {MAS_API_URL}")
    try:
        resp = http_requests.post(MAS_API_URL, json=request_body, timeout=30)
        print(f"       HTTP {resp.status_code}")
        sync_body = resp.json() if resp.headers.get("content-type", "").startswith("application/json") else resp.text
    except Exception as e:
        print(f"\n[FAIL] 请求发送失败: {e}")
        server.stop()
        sys.exit(1)

    sync_path = os.path.join(SOURCE_DATA_DIR, f"{request_id}_sync_response.json")
    with open(sync_path, "w", encoding="utf-8") as f:
        json.dump(sync_body if isinstance(sync_body, (dict, list)) else {"raw": sync_body}, f, ensure_ascii=False, indent=2)
    print(f"       已保存同步响应 -> {sync_path}")

    print(f"[4/6] 等待回调 (超时 {CALLBACK_TIMEOUT_SECONDS}s)...")
    result = server.wait_for_result(request_id, timeout=CALLBACK_TIMEOUT_SECONDS)
    server.stop()

    if result is None:
        print(f"\n[FAIL] 回调超时，未在 {CALLBACK_TIMEOUT_SECONDS}s 内收到结果")
        print("       请确认:")
        print(f"       - MAS 服务是否在 localhost:8000 运行")
        print(f"       - MAS 是否能访问回调地址 {callback_url}")
        sys.exit(1)

    callback_path = os.path.join(SOURCE_DATA_DIR, f"{request_id}_callback_response.json")
    with open(callback_path, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    items = result.get("data", {}).get("data", {}).get("items", [])
    print(f"\n[5/6] 链路测通!")
    print(f"       Response code: {result.get('code')}")
    print(f"       items 数量: {len(items)}")
    print(f"       回调 Response -> {callback_path}")

    if items:
        print_record(items)

        print(f"\n[6/6] 保存概览记录...")
        record = build_record(items, request_id, timestamp)
        record_path = os.path.join(RECORD_DIR, f"{request_id}_record.json")
        with open(record_path, "w", encoding="utf-8") as f:
            json.dump(record, f, ensure_ascii=False, indent=2)
        print(f"       已保存 -> {record_path}")


if __name__ == "__main__":
    main()
