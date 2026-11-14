# Web service: the page, the JSON API and hybrid search (no GPU).
# The language model runs in a separate private service (deploy/llm/Dockerfile);
# its address is given with the LLM_URL environment variable.
# Deploy steps: docs/deploy/app-deploy-guide.md
FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY config/ config/
COPY prompts/ prompts/
COPY src/ src/
COPY data/manifest.csv data/manifest.csv

EXPOSE 8080
CMD ["python", "-m", "src.app.server"]
