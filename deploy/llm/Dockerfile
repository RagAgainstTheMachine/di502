# Language model service: Ollama on Cloud Run with an NVIDIA L4 GPU (private).
# The model is pulled at build time and stored in the image.
# MODEL must match models.llm.name in config/rag.yaml.
# Deploy steps: docs/deploy/app-deploy-guide.md
FROM ollama/ollama:latest

ENV OLLAMA_HOST=0.0.0.0:8080 \
    OLLAMA_MODELS=/models \
    OLLAMA_KEEP_ALIVE=-1 \
    OLLAMA_NUM_PARALLEL=4 \
    MODEL=qwen3:8b

RUN ollama serve & \
    for i in $(seq 1 30); do ollama list >/dev/null 2>&1 && break; sleep 1; done; \
    ollama pull $MODEL

ENTRYPOINT ["ollama", "serve"]
