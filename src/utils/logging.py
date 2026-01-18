import logging
import os
from contextvars import ContextVar
from typing import Any, Dict
from pathlib import Path

_LOG_CONTEXT: ContextVar[Dict[str, Any]] = ContextVar("log_context", default={})


class _ContextAdapter(logging.LoggerAdapter):
    def process(self, msg, kwargs):
        extra = kwargs.get("extra", {})
        # Avoid error if extra is None
        if self.extra is None:
            self.extra = {}

        merged = {**self.extra, **_LOG_CONTEXT.get(), **extra}
        kwargs["extra"] = merged
        return msg, {"extra": kwargs}


def bind_context(**ctx: Any) -> None:
    current = _LOG_CONTEXT.get()
    _LOG_CONTEXT.set({**current, **ctx})


def clear_context() -> None:
    _LOG_CONTEXT.set({})


def configure_logging(
    level: str | None = None,
    to_file: str | None = None,
    enable_console: bool | None = None,
    log_dir: str = str(Path(__file__).resolve().parents[2] / "logs"),
) -> None:
    env_level = os.environ.get("LOG_LEVEL", None)
    env_file = os.environ.get("LOG_FILE", None)

    level_value = (level or env_level or "INFO").upper()
    enable_console_value = enable_console if enable_console is not None else False
    file_path = to_file or env_file or os.path.join(log_dir, "app.log")

    os.makedirs(log_dir, exist_ok=True)

    root = logging.getLogger()
    root.setLevel(level_value)
    for handler in list(root.handlers):
        root.removeHandler(handler)

    formatter = logging.Formatter(
        fmt="%(asctime)s %(levelname)s %(name)s %(message)s | metadata=%(extra)s",
        datefmt="%Y-%m-%dT%H:%M:%S%z",
    )

    file_handler = logging.FileHandler(file_path, encoding="utf-8")
    file_handler.setFormatter(formatter)
    root.addHandler(file_handler)

    if enable_console_value:
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        root.addHandler(console_handler)


def get_logger(name: str, **static_context: Any) -> logging.LoggerAdapter:
    logger = logging.getLogger(name)
    return _ContextAdapter(logger, static_context)
