"""DI502 trial deploy: one container with a web page, BM25 search and a small
Ollama model on CPU. Standard library only, no pip install.

Simple chunking: paragraphs are joined up to CHUNK_CHARS characters; each chunk
keeps the last heading above it as its section.

Run on Cloud Run: see deploy/trial/Dockerfile.
Run on a laptop (Ollama installed, model pulled):
    set DATA_DIR=..\\..\\data\\text
    python app.py            then open http://localhost:8080
"""
from __future__ import annotations

import json
import math
import os
import re
import shutil
import subprocess
import threading
import time
import urllib.request
from collections import Counter
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

HERE = Path(__file__).resolve().parent
DATA_DIR = Path(os.environ.get("DATA_DIR", HERE / "data" / "text"))
MODEL = os.environ.get("MODEL", "qwen2.5:1.5b")
OLLAMA = os.environ.get("OLLAMA_URL", "http://127.0.0.1:11434")
PORT = int(os.environ.get("PORT", "8080"))
K = int(os.environ.get("TOP_K", "4"))
CHUNK_CHARS = int(os.environ.get("CHUNK_CHARS", "900"))

DECLINE = ("Bu soruya yüklü belgelerden cevap veremiyorum. Kurumunuza özel değerlendirme veya güncel "
           "bilgi için Millî Teknoloji ve Yapay Zekâ Genel Müdürlüğüne başvurabilirsiniz.")

PROMPT = """Sen Türkiye'nin yapay zekâ politikası belgeleri hakkında soruları cevaplayan bir asistansın.
Kurallar:
1. Yalnızca aşağıdaki KAYNAKLAR'daki bilgiyi kullan. Kendi bilgini ekleme.
2. Türkçe ve kısa cevap ver (en fazla 5 cümle).
3. Her cümlenin sonuna dayandığı kaynağın numarasını köşeli parantezle yaz, örneğin [2].
4. Kaynaklar soruyu cevaplamıyorsa yalnızca CEVAP_YOK yaz.

KAYNAKLAR:
{sources}

SORU: {question}
CEVAP:"""


# ---------- documents and chunks ----------

def load_chunks(folder: Path) -> list[dict]:
    chunks = []
    for path in sorted(folder.glob("doc*.md")):
        text = path.read_text(encoding="utf-8")
        title = path.stem
        if text.startswith("---"):
            end = text.find("\n---", 3)
            m = re.search(r'^title:\s*"?(.*?)"?\s*$', text[:end], re.M)
            title = m.group(1) if m else title
            text = text[end + 4:]
        doc_id = path.stem.split("_")[0].capitalize()
        section, buf, buf_section = title, [], title

        def flush():
            if buf:
                chunks.append({"doc": doc_id, "title": title, "section": buf_section,
                               "text": "\n".join(buf)})
                buf.clear()

        for para in re.split(r"\n\s*\n", text):
            para = re.sub(r"<!--.*?-->", "", para, flags=re.S).strip()
            if not para:
                continue
            h = re.match(r"^(#{1,4})\s+(.*)", para)
            if h:
                section = h.group(2).strip()
            if sum(len(p) for p in buf) + len(para) > CHUNK_CHARS:
                flush()
            if not buf:
                buf_section = section
            buf.append(para)
        flush()
    return chunks


# ---------- BM25 with 5-letter prefixes ----------

def tokens(s: str) -> list[str]:
    s = s.replace("I", "ı").replace("İ", "i").lower()
    return [w[:5] for w in re.findall(r"\w+", s)]


class BM25:
    def __init__(self, docs: list[str], k1: float = 1.5, b: float = 0.75):
        self.tf = [Counter(tokens(d)) for d in docs]
        self.len = [sum(t.values()) for t in self.tf]
        self.avg = sum(self.len) / len(self.len)
        df = Counter(w for t in self.tf for w in t)
        n = len(docs)
        self.idf = {w: math.log(1 + (n - f + 0.5) / (f + 0.5)) for w, f in df.items()}
        self.k1, self.b = k1, b

    def top(self, query: str, k: int) -> list[int]:
        q = set(tokens(query))
        scores = []
        for i, tf in enumerate(self.tf):
            s = 0.0
            for w in q:
                f = tf.get(w)
                if f:
                    s += self.idf[w] * f * (self.k1 + 1) / (
                        f + self.k1 * (1 - self.b + self.b * self.len[i] / self.avg))
            scores.append(s)
        return sorted(range(len(scores)), key=lambda i: -scores[i])[:k]


# ---------- language model ----------

def generate(prompt: str) -> str:
    body = json.dumps({"model": MODEL, "prompt": prompt, "stream": False,
                       "options": {"temperature": 0, "num_ctx": 4096, "num_predict": 300}})
    req = urllib.request.Request(f"{OLLAMA}/api/generate", data=body.encode("utf-8"),
                                 headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=280) as r:
        return json.loads(r.read())["response"].strip()


def start_ollama():
    """Start Ollama inside the container (skipped if it is already running)."""
    try:
        urllib.request.urlopen(f"{OLLAMA}/api/tags", timeout=2)
        return
    except Exception:
        pass
    if shutil.which("ollama"):
        subprocess.Popen(["ollama", "serve"])
        for _ in range(60):
            try:
                urllib.request.urlopen(f"{OLLAMA}/api/tags", timeout=2)
                break
            except Exception:
                time.sleep(1)
    try:  # load the model into memory before the first question
        generate("Merhaba")
        print("model ready", flush=True)
    except Exception as e:
        print(f"warm-up failed: {e}", flush=True)


CHUNKS = load_chunks(DATA_DIR)
INDEX = BM25([c["title"] + " " + c["section"] + " " + c["text"] for c in CHUNKS])
print(f"{len(CHUNKS)} chunks from {len({c['doc'] for c in CHUNKS})} documents, model {MODEL}", flush=True)


def answer(question: str) -> dict:
    t0 = time.perf_counter()
    top = [CHUNKS[i] for i in INDEX.top(question, K)]
    sources = "\n\n".join(f"[{n}] ({c['title']} | {c['section']})\n{c['text']}"
                          for n, c in enumerate(top, 1))
    raw = generate(PROMPT.format(sources=sources, question=question))
    cited = sorted({int(x) for x in re.findall(r"\[(\d+)\]", raw) if 1 <= int(x) <= len(top)})
    declined = "CEVAP_YOK" in raw or not cited
    return {
        "answer": DECLINE if declined else raw,
        "declined": declined,
        "sources": [] if declined else [{"n": n, "doc": top[n - 1]["doc"], "title": top[n - 1]["title"],
                                         "section": top[n - 1]["section"]} for n in cited],
        "seconds": round(time.perf_counter() - t0, 1),
        "model": MODEL,
    }


# ---------- web ----------

PAGE = """<!doctype html><html lang="tr"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>DI502 deneme</title>
<style>
body{font-family:system-ui,sans-serif;max-width:760px;margin:40px auto;padding:0 16px;color:#222}
textarea{width:100%;height:80px;font:inherit;padding:8px;box-sizing:border-box}
button{margin-top:8px;padding:8px 18px;font:inherit;cursor:pointer}
#out{margin-top:24px;white-space:pre-wrap;line-height:1.5}
.src{font-size:.9em;color:#555;margin-top:12px}.meta{font-size:.8em;color:#888;margin-top:8px}
</style></head><body>
<h2>Türkiye YZ politikası belgeleri: soru-cevap (deneme)</h2>
<p class="meta">Deneme sürümü: küçük model (__MODEL__), CPU, basit parçalama. Cevaplar doğrulanmamıştır.</p>
<textarea id="q" placeholder="Örnek: Kişisel verilerin işlenme şartları nelerdir?"></textarea>
<button id="b">Sor</button>
<div id="out"></div>
<script>
const b=document.getElementById('b'),out=document.getElementById('out');
b.onclick=async()=>{const q=document.getElementById('q').value.trim();if(!q)return;
b.disabled=true;out.textContent='Cevap hazırlanıyor (ilk soru bir dakikayı bulabilir)...';
try{const r=await fetch('api/ask',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({question:q})});
const d=await r.json();if(d.error){out.textContent='Hata: '+d.error;return;}
out.textContent=d.answer;
if(d.sources.length){const s=document.createElement('div');s.className='src';
s.textContent='Kaynaklar:\\n'+d.sources.map(x=>'['+x.n+'] '+x.title+' | '+x.section).join('\\n');out.appendChild(s);}
const m=document.createElement('div');m.className='meta';m.textContent=d.seconds+' sn · '+d.model;out.appendChild(m);
}catch(e){out.textContent='Hata: '+e}finally{b.disabled=false}};
</script></body></html>"""


class Handler(BaseHTTPRequestHandler):
    def _send(self, code: int, body: bytes, ctype: str):
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        if self.path in ("/", "/index.html"):
            self._send(200, PAGE.replace("__MODEL__", MODEL).encode("utf-8"), "text/html; charset=utf-8")
        elif self.path == "/healthz":
            self._send(200, b"ok", "text/plain")
        else:
            self._send(404, b"not found", "text/plain")

    def do_POST(self):
        if self.path != "/api/ask":
            return self._send(404, b"not found", "text/plain")
        try:
            data = json.loads(self.rfile.read(int(self.headers.get("Content-Length", 0))) or b"{}")
            q = str(data.get("question", "")).strip()[:500]
            result = answer(q) if q else {"error": "soru boş"}
            code = 200
        except Exception as e:
            result, code = {"error": str(e)}, 500
        # The question text is not logged (no personal data in logs); only time and outcome.
        print(f"ask seconds={result.get('seconds')} declined={result.get('declined')}", flush=True)
        self._send(code, json.dumps(result, ensure_ascii=False).encode("utf-8"), "application/json")

    def log_message(self, *args):  # silence default access log (it would include paths only)
        pass


if __name__ == "__main__":
    threading.Thread(target=start_ollama, daemon=True).start()
    print(f"listening on :{PORT}", flush=True)
    ThreadingHTTPServer(("0.0.0.0", PORT), Handler).serve_forever()
