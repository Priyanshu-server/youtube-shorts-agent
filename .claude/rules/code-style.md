---
paths:
  - "**/*.py"
---

# Code Style

- Double quotes for all strings.
- Type-hint every function signature (params + return) and every dataclass field.
- Use `@dataclass` for data containers, `TypedDict` for LangGraph state — not plain classes.
- `snake_case` for functions/variables/files, `PascalCase` for classes/dataclasses/TypedDicts.
- Import order: stdlib, then third-party, then local (`from src...`), separated by blank lines. No wildcard imports.
- One logger per module: `log = get_logger(__name__, component="...")`. Never `logging.getLogger` directly.
- Log calls: short lowercase message, details go in `extra={...}`, not interpolated into the message string.
- Docstrings only when the function name doesn't already say what it does — one line max, no multi-line docstrings.
- Break up long files with section comments (`# Helper functions`, `# Main Function`) instead of splitting into many tiny modules.
- Env-derived dataclass defaults: `field(default_factory=lambda: os.getenv("X", default))`.
