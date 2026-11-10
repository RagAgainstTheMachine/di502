# DI502 trial deploy: web page + BM25 search + small Ollama model, CPU only, one Cloud Run service.
# Before building, copy the document texts next to this file:  data\text\doc*.md
FROM ollama/ollama:latest

RUN apt-get update && apt-get install -y --no-install-recommends python3 \
    && rm -rf /var/lib/apt/lists/*

ENV OLLAMA_HOST=127.0.0.1:11434 \
    OLLAMA_MODELS=/models \
    OLLAMA_KEEP_ALIVE=-1 \
    OLLAMA_NUM_PARALLEL=1 \
    MODEL=qwen2.5:1.5b \
    PYTHONUNBUFFERED=1

# The model is pulled at build time and stored in the image.
RUN ollama serve & \
    for i in $(seq 1 30); do ollama list >/dev/null 2>&1 && break; sleep 1; done; \
    ollama pull $MODEL

WORKDIR /app
COPY app.py ./
COPY data/text/ ./data/text/

ENTRYPOINT ["python3", "/app/app.py"]
