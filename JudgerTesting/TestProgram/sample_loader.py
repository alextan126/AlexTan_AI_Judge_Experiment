import os
import json
from typing import List, Dict, Any

from config import SAMPLES_DIR


def load_all_samples() -> List[Dict[str, Any]]:
    """加载 Samples/ 目录下所有 .json 文件，按文件名排序返回。"""
    if not os.path.isdir(SAMPLES_DIR):
        raise FileNotFoundError(f"Samples 目录不存在: {SAMPLES_DIR}")

    samples = []
    for filename in sorted(os.listdir(SAMPLES_DIR)):
        if not filename.endswith(".json"):
            continue
        filepath = os.path.join(SAMPLES_DIR, filename)
        with open(filepath, "r", encoding="utf-8") as f:
            sample = json.load(f)
        sample["_source_file"] = filename
        samples.append(sample)

    if not samples:
        raise FileNotFoundError(f"Samples 目录中没有找到 .json 文件: {SAMPLES_DIR}")

    return samples


def validate_sample(sample: Dict[str, Any]) -> List[str]:
    """校验样本格式，返回错误信息列表（空列表表示合法）。"""
    errors = []
    for field in ("sample_id", "request", "ground_truth"):
        if field not in sample:
            errors.append(f"缺少顶层字段: {field}")

    request = sample.get("request", {})
    if "data" not in request:
        errors.append("request 中缺少 data 字段")
    elif "items" not in request.get("data", {}):
        errors.append("request.data 中缺少 items 字段")

    gt = sample.get("ground_truth", {})
    if "items" not in gt:
        errors.append("ground_truth 中缺少 items 字段")

    return errors
