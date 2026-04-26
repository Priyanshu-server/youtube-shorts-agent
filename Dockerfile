FROM python:3.12-slim

WORKDIR /app

ENV VIRTUAL_ENV=/app/.venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

RUN apt-get update \
    && apt-get install -y --no-install-recommends curl ca-certificates \
    && rm -rf /var/lib/apt/lists/*

RUN curl -LsSf https://astral.sh/uv/install.sh | sh

COPY pyproject.toml uv.lock* ./

RUN /root/.local/bin/uv venv "$VIRTUAL_ENV" \
    && /root/.local/bin/uv sync --frozen

COPY . /app

CMD ["python"]
