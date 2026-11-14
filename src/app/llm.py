"""Call the language model (Ollama API), locally or on a private Cloud Run service.

LLM_URL selects the model server:
  http://localhost:11434            Ollama on this computer
  http://localhost:9090             `gcloud run services proxy di502-llm --port 9090`
  https://di502-llm-....run.app     the private Cloud Run service; an identity token
                                    from the metadata server is added automatically
"""
from __future__ import annotations

import json
import os
import re
import time
import urllib.parse
import urllib.request

from src.shared.common import CONFIG

LLM = CONFIG["models"]["llm"]
LLM_URL = os.getenv("LLM_URL", "http://localhost:11434").rstrip("/")
_TOKEN = {"value": "", "expires": 0.0}


def _identity_token(audience: str) -> str:
    """Google identity token for calling a private Cloud Run service (empty when not on GCP)."""
    if time.time() < _TOKEN["expires"]:
        return _TOKEN["value"]
    url = ("http://metadata.google.internal/computeMetadata/v1/instance/service-accounts/default/"
           "identity?audience=" + urllib.parse.quote(audience, safe=""))
    try:
        req = urllib.request.Request(url, headers={"Metadata-Flavor": "Google"})
        with urllib.request.urlopen(req, timeout=3) as r:
            _TOKEN.update(value=r.read().decode(), expires=time.time() + 45 * 60)
    except OSError:
        _TOKEN.update(value="", expires=time.time() + 5 * 60)
    return _TOKEN["value"]


def generate(prompt: str, url: str = LLM_URL) -> str:
    body = {"model": LLM["name"], "prompt": prompt, "stream": False,
            "options": {"temperature": LLM["temperature"], "num_ctx": LLM["context_tokens"],
                        "num_predict": LLM["max_tokens"]}}
    if LLM.get("think") is not None:
        body["think"] = bool(LLM["think"])  # qwen3: false turns the reasoning text off
    headers = {"Content-Type": "application/json"}
    if url.startswith("https://"):
        token = _identity_token(url)
        if token:
            headers["Authorization"] = f"Bearer {token}"
    req = urllib.request.Request(f"{url}/api/generate", data=json.dumps(body).encode("utf-8"),
                                 headers=headers, method="POST")
    with urllib.request.urlopen(req, timeout=LLM["timeout_seconds"]) as r:
        text = json.loads(r.read())["response"]
    # Safety net if the model still writes a reasoning block.
    return re.sub(r"<think>.*?</think>", "", text, flags=re.S).strip()
