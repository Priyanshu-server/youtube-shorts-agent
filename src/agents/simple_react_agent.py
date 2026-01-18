from src.utils.models import get_model
from src.utils.logging import get_logger
from src.utils.cust_types import Agent
from typing import Dict, Any


log = get_logger(__name__, component="agent")


def get_agent(
    agent_name: str,
    model_parent: str,
    model_name: str,
    model_args: dict,
    model_kwargs: dict,
    metadata: Dict[str, Any] = {},
    *agent_args,
    **agent_kwargs,
) -> Agent:
    """Factory function to create an Agent instance."""
    log.debug(
        "building agent",
        extra={"agent_name": agent_name, "model_parent": model_parent, "model_name": model_name},
    )
    model = get_model(model_name, model_parent, *model_args, **model_kwargs)
    # TODO : Agent Creation

    return Agent(
        agent_name=agent_name,
        model=model,
        metadata=metadata,
    )
