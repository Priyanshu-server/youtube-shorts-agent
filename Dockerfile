FROM python:3.12-slim

WORKDIR /app

ENV VIRTUAL_ENV=/app/.venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

RUN apt-get update \
    && apt-get install -y --no-install-recommends curl ca-certificates \
    && rm -rf /var/lib/apt/lists/*

RUN curl -LsSf https://astral.sh/uv/install.sh | sh

COPY . /app

RUN /root/.local/bin/uv venv "$VIRTUAL_ENV" \
    && if [ ! -f pyproject.toml ]; then \
         /root/.local/bin/uv init -q; \
       fi \
    && if [ -f uv.lock ]; then \
         /root/.local/bin/uv sync --frozen; \
       elif [ -f pyproject.toml ]; then \
         /root/.local/bin/uv sync; \
       elif [ -f requirements.txt ]; then \
         /root/.local/bin/uv pip install -r requirements.txt; \
       fi \
    && /root/.local/bin/uv add langgraph langchain

CMD ["python"]
