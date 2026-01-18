from dataclasses import dataclass
from typing import Dict, List, Any

# 3rd party types
from datetime import datetime, timezone
from langchain.messages import AIMessage, HumanMessage

# Custom Types for basic processing


@dataclass(repr=True)
class URLType:
    url: str
    title: str
    created_time: datetime

    def __post_init__(self):
        if not self.created_time:
            self.created_time = datetime.now(timezone.utc)

    def __str__(self):
        return f"URLType(title={self.title}, url={self.url}, created_time={self.created_time})"


# Custom Types related to Agents


@dataclass(repr=True)
class AgentOutputMetadata:
    tool_called: bool
    message: str


@dataclass(repr=True)
class AgentOutput:
    response: str
    action: Dict[str, Any]
    message_history: List[
        AIMessage | HumanMessage
    ]  # Optional (either AIMessage or HumanMessage)
    metadata: AgentOutputMetadata
    success: bool
