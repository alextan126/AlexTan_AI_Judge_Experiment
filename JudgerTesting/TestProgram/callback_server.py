import json
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
from typing import Dict, Any, Optional

from config import CALLBACK_HOST, CALLBACK_PORT, CALLBACK_TIMEOUT_SECONDS


class _CallbackStore:
    """线程安全的回调结果存储。"""

    def __init__(self):
        self._lock = threading.Lock()
        self._results: Dict[str, Any] = {}
        self._events: Dict[str, threading.Event] = {}

    def register(self, request_id: str) -> threading.Event:
        """注册一个待接收的回调，返回对应的 Event 供等待。"""
        event = threading.Event()
        with self._lock:
            self._events[request_id] = event
        return event

    def put(self, request_id: str, data: Any):
        """存入回调结果并触发 Event。"""
        with self._lock:
            self._results[request_id] = data
            event = self._events.get(request_id)
        if event:
            event.set()

    def get(self, request_id: str) -> Optional[Any]:
        with self._lock:
            return self._results.pop(request_id, None)

    def cleanup(self, request_id: str):
        with self._lock:
            self._results.pop(request_id, None)
            self._events.pop(request_id, None)


callback_store = _CallbackStore()


class _CallbackHandler(BaseHTTPRequestHandler):

    def do_POST(self):
        # URL 格式: /callback/{request_id}
        parts = self.path.strip("/").split("/")
        if len(parts) >= 2 and parts[0] == "callback":
            request_id = parts[1]
        else:
            self.send_response(400)
            self.end_headers()
            self.wfile.write(b'{"error": "invalid callback path"}')
            return

        content_length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(content_length)
        try:
            data = json.loads(body)
        except json.JSONDecodeError:
            self.send_response(400)
            self.end_headers()
            self.wfile.write(b'{"error": "invalid json"}')
            return

        callback_store.put(request_id, data)

        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(b'{"status": "received"}')

    def log_message(self, format, *args):
        pass  # 静默日志，避免污染测试输出


class CallbackServer:
    """在后台线程运行的本地 HTTP 回调服务器。"""

    def __init__(self, host: str = CALLBACK_HOST, port: int = CALLBACK_PORT):
        self.host = host
        self.port = port
        self._httpd: Optional[HTTPServer] = None
        self._thread: Optional[threading.Thread] = None

    @property
    def base_url(self) -> str:
        return f"http://{self.host}:{self.port}"

    def callback_url(self, request_id: str) -> str:
        return f"{self.base_url}/callback/{request_id}"

    def start(self):
        self._httpd = HTTPServer((self.host, self.port), _CallbackHandler)
        self._thread = threading.Thread(target=self._httpd.serve_forever, daemon=True)
        self._thread.start()

    def stop(self):
        if self._httpd:
            self._httpd.shutdown()
            self._httpd = None

    def wait_for_result(
        self, request_id: str, timeout: float = CALLBACK_TIMEOUT_SECONDS
    ) -> Optional[Any]:
        """阻塞等待指定 request_id 的回调结果，超时返回 None。"""
        event = callback_store.register(request_id)
        arrived = event.wait(timeout=timeout)
        if arrived:
            return callback_store.get(request_id)
        callback_store.cleanup(request_id)
        return None
