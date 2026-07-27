"""Local API Server — safe-local HTTP server for mobile clients.

Uses Python stdlib only (http.server). No external dependencies.
Binds 127.0.0.1 by default. Never 0.0.0.0 without explicit approval.
"""

from __future__ import annotations

import json
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
from pathlib import Path

from hermes_core.mobile_gateway.contract import MobileAPIEndpoint, MobileAPIResponse
from hermes_core.mobile_gateway.gateway import MobileGateway


class MobileAPIRequestHandler(BaseHTTPRequestHandler):
    """HTTP request handler for mobile API.

    Routes GET/POST to MobileGateway.
    All responses are JSON with safety metadata.
    """

    gateway: MobileGateway = MobileGateway()  # class-level singleton

    # ── Routing table ──
    _ROUTES: dict[tuple[str, str], MobileAPIEndpoint] = {
        ("GET", "/api/status"): MobileAPIEndpoint.STATUS,
        ("GET", "/api/dashboard"): MobileAPIEndpoint.DASHBOARD,
        ("GET", "/api/daily-report"): MobileAPIEndpoint.DAILY_REPORT,
        ("GET", "/api/daily-assistant"): MobileAPIEndpoint.DAILY_ASSISTANT,
        ("GET", "/api/what-next"): MobileAPIEndpoint.WHAT_NEXT,
        ("GET", "/api/local-health"): MobileAPIEndpoint.LOCAL_HEALTH,
        ("GET", "/api/malyarka/status"): MobileAPIEndpoint.MALYARKA_STATUS,
        ("POST", "/api/malyarka/dialog"): MobileAPIEndpoint.MALYARKA_DIALOG,
        ("GET", "/api/ai-provider/status"): MobileAPIEndpoint.AI_PROVIDER_STATUS,
        ("GET", "/api/bridge/status"): MobileAPIEndpoint.BRIDGE_STATUS,
        ("POST", "/api/bridge/route"): MobileAPIEndpoint.BRIDGE_ROUTE,
    }

    def _send_json(self, response: MobileAPIResponse, code: int = 200) -> None:
        """Send a JSON response with CORS and safety headers."""
        body = json.dumps(response.to_dict(), ensure_ascii=False, indent=2)
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("X-Hermes-Mode", "safe-local")
        self.send_header("X-Bind-Address", "127.0.0.1")
        self.send_header("Content-Length", str(len(body.encode("utf-8"))))
        self.end_headers()
        self.wfile.write(body.encode("utf-8"))

    def do_OPTIONS(self) -> None:
        """CORS preflight."""
        self.send_response(204)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_GET(self) -> None:
        """Handle GET request."""
        path = self.path.rstrip("/") or "/"
        endpoint = self._ROUTES.get(("GET", path))

        if endpoint is None:
            resp = MobileAPIResponse.blocked(
                endpoint=f"GET {path}",
                action="unknown",
                reason=f"Unknown GET endpoint. Available: {[r[1] for r in self._ROUTES if r[0] == 'GET']}",
            )
            self._send_json(resp, 404)
            return

        # Check if blocked
        from hermes_core.mobile_gateway.contract import BLOCKED_ENDPOINTS
        if endpoint in BLOCKED_ENDPOINTS:
            resp = MobileAPIResponse.blocked(
                endpoint=f"GET {path}",
                action=endpoint.name,
                reason="This endpoint is permanently blocked in safe-local mode.",
            )
            self._send_json(resp, 403)
            return

        resp = self.gateway.handle(endpoint)
        self._send_json(resp)

    def do_POST(self) -> None:
        """Handle POST request."""
        path = self.path.rstrip("/") or "/"
        endpoint = self._ROUTES.get(("POST", path))

        if endpoint is None:
            resp = MobileAPIResponse.blocked(
                endpoint=f"POST {path}",
                action="unknown",
                reason=f"Unknown POST endpoint. Available: {[r[1] for r in self._ROUTES if r[0] == 'POST']}",
            )
            self._send_json(resp, 404)
            return

        # Read payload
        content_length = int(self.headers.get("Content-Length", 0))
        payload = {}
        if content_length > 0:
            try:
                body = self.rfile.read(content_length)
                payload = json.loads(body)
            except (json.JSONDecodeError, Exception):
                pass

        resp = self.gateway.handle(endpoint, payload)
        self._send_json(resp)

    def log_message(self, format: str, *args) -> None:
        """Suppress default logging — we don't log requests in safe mode."""
        pass  # No logging in safe-local mode


class LocalAPIServer:
    """Safe-local HTTP API server.

    Binds to 127.0.0.1 by default.
    Never binds to 0.0.0.0 without explicit approval.
    No firewall changes. No external network.
    """

    DEFAULT_HOST = "127.0.0.1"
    DEFAULT_PORT = 8514  # Hermes → H(8) E(5) R(1) ... 8514

    def __init__(self, host: str | None = None, port: int | None = None) -> None:
        self.host = host or self.DEFAULT_HOST
        self.port = port or self.DEFAULT_PORT
        self._server: HTTPServer | None = None
        self._thread: threading.Thread | None = None

    @property
    def is_running(self) -> bool:
        return self._server is not None

    @property
    def bind_address(self) -> str:
        return f"{self.host}:{self.port}"

    def start(self, block: bool = False) -> None:
        """Start the server.

        Args:
            block: If True, blocks the current thread. Default False (runs in background).
        """
        if self._server is not None:
            return

        # Safety: enforce 127.0.0.1
        if self.host not in ("127.0.0.1", "localhost"):
            raise ValueError(
                f"Cannot bind to {self.host}. "
                f"Mobile API server must bind to 127.0.0.1 in safe-local mode."
            )

        self._server = HTTPServer((self.host, self.port), MobileAPIRequestHandler)
        self._server.timeout = 1  # 1-second timeout for clean shutdown

        if block:
            self._server.serve_forever()
        else:
            self._thread = threading.Thread(target=self._server.serve_forever, daemon=True)
            self._thread.start()

    def stop(self) -> None:
        """Stop the server."""
        if self._server is not None:
            self._server.shutdown()
            self._server.server_close()
            self._server = None
        self._thread = None

    def self_check(self) -> bool:
        """Quick self-check: start, make a request, stop.

        Returns True if the server is functional.
        """
        import urllib.request

        try:
            self.start()
            url = f"http://{self.host}:{self.port}/api/status"
            with urllib.request.urlopen(url, timeout=3) as resp:
                data = json.loads(resp.read())
                ok = data.get("status") == "OK"
            self.stop()
            return ok
        except Exception:
            try:
                self.stop()
            except Exception:
                pass
            return False
