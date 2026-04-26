from dataclasses import dataclass
from dataclasses import field
from typing import Dict, Any, Callable, Optional

# 3rd party types
from datetime import datetime, timezone
from langgraph.graph.state import CompiledStateGraph

# Custom Types for basic processing


@dataclass(repr=True)
class URLType:
    url: str
    title: str
    created_time: datetime | None = None

    def __post_init__(self):
        if not self.created_time:
            self.created_time = datetime.now(timezone.utc)

    def __str__(self):
        return f"URLType(title={self.title}, url={self.url}, created_time={self.created_time})"


# Custom Types related to Agents


@dataclass(repr=True)
class Model:
    model_name: str
    model_parent: str
    model: Any


@dataclass(repr=True)
class Agent:
    agent_name: str
    agent_description: str
    inputs: Dict[str, str]                              # key → prompt text shown to user
    factory: Callable[[], CompiledStateGraph]           # builds a fresh graph per run
    build_graph_input: Callable[[Dict[str, str]], Dict[str, Any]]  # maps collected inputs → graph input dict
    output_key: str                                     # key to read from graph output
    graph: Optional[CompiledStateGraph] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    created_time: datetime | None = None

    def __post_init__(self):
        if not self.created_time:
            self.created_time = datetime.now(timezone.utc)

    def __str__(self):
        return f"Agent(agent_name={self.agent_name}, metadata={self.metadata}, created_time={self.created_time})"
