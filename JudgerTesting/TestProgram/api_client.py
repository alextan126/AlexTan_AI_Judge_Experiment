import copy
import requests
from typing import Dict, Any, Optional

from config import MAS_API_URL


def send_review_request(
    sample: Dict[str, Any],
    callback_url: str,
    round_index: int,
    timeout: float = 30.0,
) -> Optional[Dict[str, Any]]:
    """
    向 MAS Review API 发送一次审题请求。

    基于样本的 request 模板构造实际请求体，替换 callback 和 business_id。
    返回 API 的同步响应（通常只是确认收到），若请求失败返回 None。
    """
    request_body = copy.deepcopy(sample["request"])

    sample_id = sample["sample_id"]
    request_id = f"{sample_id}_round{round_index}"

    request_body["callback"] = callback_url
    request_body["business_id"] = request_id

    try:
        resp = requests.post(
            MAS_API_URL,
            json=request_body,
            timeout=timeout,
        )
        resp.raise_for_status()
        return {"request_id": request_id, "status_code": resp.status_code, "body": resp.json()}
    except requests.RequestException as e:
        return {"request_id": request_id, "status_code": None, "error": str(e)}
