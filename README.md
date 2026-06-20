# YouTube Shorts Agent

An interactive AI agent for YouTube Shorts generation, powered by LangGraph and OpenAI.

## Prerequisites

- **Normal run:** Python 3.12+ and [uv](https://github.com/astral-sh/uv)
- **Docker run:** Docker

## Environment Variables

Copy `.env.example` to `.env` and fill in the values:

```bash
cp .env.example .env
```

| Variable | Required | Description |
|---|---|---|
| `OPENAI_API_KEY` | Yes | Your OpenAI API key |
| `SERVICE_NAME` | No | Service name for logging |
| `ENV` | No | Environment name for logging |

> `settings.py` uses `python-dotenv` (`load_dotenv()`), so the `.env` file is loaded automatically in both local and Docker runs.

---

## Normal Run (local)

```bash
# Install dependencies
uv sync

# Run the agent
uv run python main.py
```

---

## Docker Run

```bash
# Build the image
docker build -t youtube-shorts-agent .

# Run with environment variables from .env file
docker run --env-file .env -it youtube-shorts-agent python main.py
```

---

## Makefile (recommended)

The project includes a `Makefile` for common tasks. Run `make` (or `make help`) to see all targets.

| Target | Description |
|---|---|
| `make install` | Install all dependencies via `uv sync` |
| `make run` | Run `main.py` via `uv` |
| `make docker-build` | Build the Docker image |
| `make docker-run` | Build image and run the container (uses `.env` file) |
| `make docker-stop` | Stop and remove the running container |
| `make clean` | Remove `__pycache__`, `.pyc` files, `.venv`, and build artifacts |

**Quick start with make:**

```bash
# Local
make install
make run

# Docker
make docker-run

# Cleanup
make clean
```

---
