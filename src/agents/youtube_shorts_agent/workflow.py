from langgraph.graph import END, START, StateGraph
from langgraph.graph.state import CompiledStateGraph
from src.utils.cust_types import Agent
from src.utils.logging import get_logger

from .agent_state import YoutubeShortsState

log = get_logger(__name__, component="youtube_shorts_agent")


def ideas_node(state: YoutubeShortsState) -> dict:
    topic = state["topic"]
    log.info("generating ideas", extra={"topic": topic})
    ideas = [
        f"Day in the life of someone obsessed with {topic}",
        f"3 things nobody tells you about {topic}",
        f"I tried {topic} for 7 days — here's what happened",
        f"The fastest way to learn {topic} in 60 seconds",
        f"Why everyone is wrong about {topic}",
    ]
    result = f"YouTube Shorts ideas for '{topic}':\n" + "\n".join(
        f"  {i + 1}. {idea}" for i, idea in enumerate(ideas)
    )
    log.info("ideas generated", extra={"topic": topic, "count": len(ideas)})
    return {"result": result}


def build_workflow() -> CompiledStateGraph:
    graph: StateGraph = StateGraph(YoutubeShortsState)
    graph.add_node("ideas", ideas_node)
    graph.add_edge(START, "ideas")
    graph.add_edge("ideas", END)
    return graph.compile()


def get_agent() -> Agent:
    return Agent(
        agent_name="Youtube Shorts Agent",
        agent_description="Generates YouTube Shorts video ideas for a given topic",
        inputs={"topic": "Enter a topic : "},
        factory=build_workflow,
        build_graph_input=lambda d: {"topic": d["topic"], "result": ""},
        output_key="result",
    )
