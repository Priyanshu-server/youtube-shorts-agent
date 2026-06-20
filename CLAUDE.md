# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project

An interactive CLI agent for YouTube Shorts idea generation, built on LangGraph + LangChain (OpenAI). The repo is structured as a small framework for registering multiple LangGraph-based agents behind one CLI entry point, with only one real agent (`youtube_shorts_agent`) currently implemented.

## Commands

```bash
uv sync                 # install dependencies (Python 3.12+, uv required)
uv run python main.py   # run the interactive CLI
make install / make run # Makefile wrappers for the above
make docker-build        # docker build -t app .
make docker-run          # build + run container with --env-file .env
make docker-stop
make clean               # remove __pycache__, .venv, build artifacts
```

There are no tests and no lint/type-check configuration in this repo (no pytest, ruff, or mypy config present). CI (`.github/workflows/docker-build.yml`) only verifies the Docker image builds on push/PR to `main`.

## Architecture

### Flow: `main.py` → `registry.py` → agent `workflow.py`

`main.py` lists every `Agent` in `registry.REGISTRY`, prompts the user to pick one, collects raw string inputs per `Agent.inputs` (a `dict[key -> prompt text]`), then runs:

```python
graph = entry.factory()                       # build a fresh CompiledStateGraph
output = graph.invoke(entry.build_graph_input(collected))
print(output[entry.output_key])
```

`bind_context(agent=entry.agent_name)` / `clear_context()` wrap the run so all log lines emitted during that agent's execution carry the agent name.

### Agent discovery (`registry.py`)

`REGISTRY` is built at import time by `pkgutil.iter_modules(src.agents.__path__)`: for every subpackage of `src/agents/`, it imports `src.agents.<name>.workflow` and calls `get_agent()` if that module defines it. **Any `ImportError` or exception during discovery is silently swallowed** — a broken or incomplete agent module just doesn't appear in the menu instead of crashing the app. Keep this in mind when an agent doesn't show up: check for import errors by importing the module directly rather than assuming it's missing.

To add a new agent: create `src/agents/<your_agent>/workflow.py` exposing `get_agent() -> Agent`, plus any state/types module it needs (see `youtube_shorts_agent/` as the reference implementation).

### The `Agent` contract (`src/utils/cust_types.py`)

```python
Agent(agent_name, agent_description, inputs, factory, build_graph_input, output_key, graph=None, metadata={}, created_time=None)
```

- `inputs`: dict of input key → prompt text shown to the user via `input()`.
- `factory`: zero-arg callable that builds and compiles a *fresh* `StateGraph` per run (see `build_workflow()` in `youtube_shorts_agent/workflow.py`).
- `build_graph_input`: maps the collected `dict[str, str]` of raw user input into the graph's initial state dict.
- `output_key`: key read out of `graph.invoke(...)`'s return dict and printed to the user.

`agent_state.py` files define the LangGraph state as a `TypedDict` (e.g. `YoutubeShortsState`).

### Prebuilt helper (`src/agents/prebuilt/simple_react_agent.py`)

A composable builder for a model+tools ReAct-style LangGraph node (`create_simple_react_node`, `get_simple_react_agent`), wrapping `src/utils/models.get_model`. It is **not** wired into the registry — `prebuilt` has no `workflow.py`/`get_agent()`, so it's never discovered. It's also currently broken if called directly: `get_simple_react_agent` constructs `Agent(agent_name=..., graph=..., model=..., metadata=...)`, but the `Agent` dataclass has no `model` field and requires `agent_description`/`inputs`/`build_graph_input`/`output_key`. Treat this module as scaffolding to adapt, not a working agent.

### Models (`src/utils/models.py`)

`get_model(model_name, model_parent, *args, **kwargs)` is the single chokepoint for constructing LLM clients, returning a `Model(model_name, model_parent, model)` wrapper. Only `model_parent == "openai"` is implemented (via `ChatOpenAI`); other parents raise `ValueError`. Add new providers by extending this function rather than instantiating LangChain chat models directly in agent code.

### Logging (`src/utils/logging.py`)

Custom context-aware logging: `get_logger(name, **static_context)` returns a `LoggerAdapter` that merges static context, a `ContextVar`-based dynamic context (set/cleared via `bind_context()`/`clear_context()`), and any per-call `extra=`. All agent/util modules log through this (`log = get_logger(__name__, component=...)`).

Log output is **only configured** when `configure_logging()` runs (file handler to `logs/app.log`, console disabled by default). That function is currently called solely from `settings.py`'s `Settings.__post_init__`, and **nothing in `main.py`/`registry.py`/the agent modules imports `settings.py`** — so running `main.py` as-is does not attach any log handlers. If you need logs during a normal run, import `settings` (or call `configure_logging()`) early, e.g. at the top of `main.py`.

### Settings (`settings.py`)

Loads `.env` via `python-dotenv` and exposes a module-level singleton `config = Settings()` reading `SERVICE_NAME`, `ENV`, `OPENAI_API_KEY` from the environment. On construction it calls `configure_logging()` and logs only boolean presence of each setting (never the values), to avoid leaking secrets.

## Environment Variables

Copy `.env.example` to `.env`. `OPENAI_API_KEY` is required for any agent that calls `get_model(..., "openai")`; `SERVICE_NAME`/`ENV` are optional and only affect logging metadata.
