from typing import Any, Annotated, TypedDict, Dict, Callable, Sequence, List

from langchain_core.messages import AnyMessage
from langchain_core.tools import BaseTool
from langgraph.graph import END, START, StateGraph
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition

from src.utils.cust_types import Agent, Model
from src.utils.logging import get_logger
from src.utils.models import get_model

log = get_logger(__name__, component="simple_react_agent")


class DynamicMessageState(TypedDict, total=False):
    messages: Annotated[list[AnyMessage], add_messages]


class ReactModelNode:
    def __init__(self, model: Model) -> None:
        self._model = model

    def validate_state(self, state: Any) -> None:
        input_messages = state.get("messages", None)
        if input_messages is None:
            raise ValueError("State must include `messages`.")

    def validate_messages(self, messages: List[Any]) -> None:
        for message in messages:
            if isinstance(message, str):
                raise ValueError(
                    "Message is of type str, only langchain_core.messages.AnyMessage type supported!"
                )

    def __call__(self, state: Any) -> dict[str, Any]:
        self.validate_state(state)
        input_messages = state.get("messages")
        self.validate_messages(messages=input_messages)

        response = self._model.model.invoke(input_messages)
        return {"messages": [response]}


# Helper functions


def _normalize_model_args(model_args: Any) -> tuple[Any, ...]:
    if not model_args:
        return ()
    if isinstance(model_args, tuple):
        return model_args
    if isinstance(model_args, list):
        return tuple(model_args)
    if isinstance(model_args, dict):
        # Backward compatibility for previous usage that passed `{}`.
        return ()
    return (model_args,)


def _normalize_tools(
    tools: Sequence[Callable[..., Any] | BaseTool] | None,
) -> list[Callable[..., Any] | BaseTool]:
    if not tools:
        return []

    normalized_tools: list[Callable[..., Any] | BaseTool] = []
    for tool in tools:
        if not callable(tool) and not isinstance(tool, BaseTool):
            raise TypeError("Each tool must be a callable or BaseTool instance.")
        normalized_tools.append(tool)
    return normalized_tools


def _get_configured_model(
    model_name: str,
    model_parent: str,
    model_args: tuple[Any, ...] | None = None,
    model_kwargs: Dict[str, Any] | None = None,
    tools: Sequence[Callable[..., Any] | BaseTool] | None = None,
) -> tuple[Model, list[Callable[..., Any] | BaseTool]]:
    model_kwargs = model_kwargs or {}
    model = get_model(
        model_name,
        model_parent,
        *_normalize_model_args(model_args),
        **model_kwargs,
    )

    normalized_tools = _normalize_tools(tools)

    if normalized_tools:
        if not hasattr(model.model, "bind_tools"):
            raise TypeError(
                f"Model `{model_name}` from `{model_parent}` does not support tool binding."
            )
        model.model = model.model.bind_tools(normalized_tools)

    return model, normalized_tools


# Public composable builders


def create_simple_react_node(
    model_parent: str,
    model_name: str,
    model_args: tuple[Any, ...] | None = None,
    model_kwargs: Dict[str, Any] | None = None,
    tools: Sequence[Callable[..., Any] | BaseTool] | None = None,
) -> tuple[ReactModelNode, Model, list[Callable[..., Any] | BaseTool]]:
    """Build a model node that can be embedded inside a larger LangGraph workflow."""

    model, normalized_tools = _get_configured_model(
        model_name=model_name,
        model_parent=model_parent,
        model_args=model_args,
        model_kwargs=model_kwargs,
        tools=tools,
    )

    node = ReactModelNode(model=model)
    return node, model, normalized_tools


# Main Function


def get_simple_react_agent(
    agent_name: str,
    model_parent: str,
    model_name: str,
    model_args: tuple[Any, ...] | None = None,
    model_kwargs: Dict[str, Any] | None = None,
    tools: Sequence[Callable[..., Any] | BaseTool] | None = None,
    metadata: dict[str, Any] | None = None,
    agent_state: StateGraph[Any] | None = None,
    *agent_args,
    **agent_kwargs,
) -> Agent:
    """Create a simple, reusable react-style agent graph."""
    del agent_args, agent_kwargs

    log.info(
        "building agent",
        extra={
            "agent_name": agent_name,
            "model_parent": model_parent,
            "model_name": model_name,
        },
    )

    node, model, normalized_tools = create_simple_react_node(
        model_parent=model_parent,
        model_name=model_name,
        model_args=model_args,
        model_kwargs=model_kwargs,
        tools=tools,
    )

    workflow: StateGraph[Any] = (
        agent_state if agent_state is not None else StateGraph(DynamicMessageState)
    )
    workflow.add_node("agent", node)
    workflow.add_edge(START, "agent")

    if normalized_tools:
        workflow.add_node("tools", ToolNode(normalized_tools))
        workflow.add_conditional_edges("agent", tools_condition)
        workflow.add_edge("tools", "agent")
    else:
        workflow.add_edge("agent", END)

    compiled_graph = workflow.compile()

    return Agent(
        agent_name=agent_name,
        graph=compiled_graph,
        model=model,
        metadata=metadata or {},
    )
