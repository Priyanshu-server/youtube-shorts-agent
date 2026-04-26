import importlib
import pkgutil

import src.agents
from src.utils.cust_types import Agent


def _discover_agents() -> list[Agent]:
    agents: list[Agent] = []
    for module_info in pkgutil.iter_modules(src.agents.__path__):
        try:
            mod = importlib.import_module(f"src.agents.{module_info.name}.workflow")
            if hasattr(mod, "get_agent"):
                agents.append(mod.get_agent())
        except (ImportError, Exception):
            pass
    return agents


REGISTRY: list[Agent] = _discover_agents()
