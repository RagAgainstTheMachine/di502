"""Web page and JSON API for the assistant.

Run from the repository root:
    python -m src.app.server            then open http://localhost:8080

Routes:
    GET  /             the page (src/app/static/index.html)
    GET  /api/config   collection date, questions per chat, model name
    POST /api/ask      {"question": "..."} -> answer or decline (see src/app/answer.py)
    GET  /healthz      "ok"

The question text is never logged; only the outcome and timings are.
Chats are kept in the browser tab only; the server stores nothing.
"""
from __future__ import annotations

import json
import os
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

from src.app.answer import answer
from src.app.catalog import collection_date
from src.shared.common import CONFIG

PAGE = (Path(__file__).parent / "static" / "index.html").read_bytes()
MAX_QUESTION_CHARS = 500


class Handler(BaseHTTPRequestHandler):
    def _send(self, code: int, body: bytes, ctype: str):
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.end_headers()
        self.wfile.write(body)

    def _json(self, code: int, obj):
        self._send(code, json.dumps(obj, ensure_ascii=False).encode("utf-8"), "application/json; charset=utf-8")

    def do_GET(self):
        if self.path in ("/", "/index.html"):
            self._send(200, PAGE, "text/html; charset=utf-8")
        elif self.path == "/api/config":
            self._json(200, {"collection_date": collection_date(),
                             "questions_per_chat": CONFIG["app"]["questions_per_chat"],
                             "model": CONFIG["models"]["llm"]["name"]})
        elif self.path == "/healthz":
            self._send(200, b"ok", "text/plain")
        else:
            self._send(404, b"not found", "text/plain")

    def do_POST(self):
        if self.path != "/api/ask":
            return self._send(404, b"not found", "text/plain")
        try:
            length = int(self.headers.get("Content-Length", 0))
            if length > 10_000:
                return self._json(413, {"error": "İstek çok büyük."})
            question = str(json.loads(self.rfile.read(length) or b"{}").get("question", "")).strip()
        except (ValueError, json.JSONDecodeError):
            return self._json(400, {"error": "Geçersiz istek."})
        if not question:
            return self._json(400, {"error": "Soru boş olamaz."})
        if len(question) > MAX_QUESTION_CHARS:
            return self._json(400, {"error": f"Soru en fazla {MAX_QUESTION_CHARS} karakter olabilir."})
        try:
            result = answer(question)
        except Exception as exc:  # search or model unreachable
            print(f"ask error={type(exc).__name__}", flush=True)
            return self._json(503, {"error": "Arama veya dil modeli servisine şu an ulaşılamıyor. "
                                             "Biraz sonra tekrar deneyin."})
        print(f"ask status={result['status']} reason={result['reason']} timing={result['timing']}", flush=True)
        self._json(200, result)

    def log_message(self, *args):
        pass  # default access log is off; see the print above


def main():
    port = int(os.getenv("PORT", "8080"))
    print(f"listening on http://localhost:{port}", flush=True)
    ThreadingHTTPServer(("0.0.0.0", port), Handler).serve_forever()


if __name__ == "__main__":
    main()
