from langchain_core.messages import HumanMessage, SystemMessage
from pydantic import BaseModel, Field

from src.agents.youtube_shorts_agent.config import MODEL_NAME, MODEL_PARENT
from src.agents.youtube_shorts_agent.prompt import PARSE_SYSTEM_PROMPT
from src.utils.models import get_model


class ParsedQuery(BaseModel):
    youtube_url: str = Field(description="The YouTube URL copied verbatim from the user's message, or empty string if none is present")
    reply: str = Field(description="A short, friendly acknowledgment of the request")


def build_query_parser():
    model = get_model(MODEL_NAME, MODEL_PARENT)
    return model.model.with_structured_output(ParsedQuery)


def parse_query(query: str) -> ParsedQuery:
    parser = build_query_parser()
    messages = [SystemMessage(content=PARSE_SYSTEM_PROMPT), HumanMessage(content=query)]
    return parser.invoke(messages)
