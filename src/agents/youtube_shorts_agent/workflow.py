import json

from langgraph.graph import END, START, StateGraph
from langgraph.graph.state import CompiledStateGraph

from src.agents.youtube_shorts_agent.agent_state import YoutubeShortsState
from src.agents.youtube_shorts_agent.utils import parse_query
from src.utils.cust_types import Agent
from src.utils.logging import get_logger

log = get_logger(__name__, component="youtube_shorts_agent")


# Graph nodes


def parse_node(state: YoutubeShortsState) -> dict:
    query = state["query"]
    log.info("parsing query", extra={"query": query})

    parsed = parse_query(query)

    result = json.dumps(parsed.model_dump(), indent=2)
    log.info("query parsed", extra={"youtube_url": parsed.youtube_url})
    return {"youtube_url": parsed.youtube_url, "reply": parsed.reply, "result": result}


def build_workflow() -> CompiledStateGraph:
    graph: StateGraph = StateGraph(YoutubeShortsState)
    graph.add_node("parse", parse_node)
    graph.add_edge(START, "parse")
    graph.add_edge("parse", END)
    return graph.compile()


# Main Function


def get_agent() -> Agent:
    return Agent(
        agent_name="Youtube Shorts Agent",
        agent_description="Extracts a YouTube link and intent from a free-form request and returns structured JSON",
        inputs={"query": "Enter your request (include the YouTube link): "},
        factory=build_workflow,
        build_graph_input=lambda d: {"query": d["query"], "youtube_url": "", "reply": "", "result": ""},
        output_key="result",
    )
