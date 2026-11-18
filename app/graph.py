
from langgraph.graph import StateGraph, START, END

from app.state import AegisState

from app.agents.requirement import requirement_agent
from app.agents.knowledge import knowledge_agent
from app.agents.planner import planner_agent
from app.agents.architecture import architecture_agent
from app.agents.code_generator import code_generator_agent
from app.agents.mcp_tools import mcp_tools_agent
from app.agents.validator import validator_agent


def build_graph():

    graph = StateGraph(AegisState)

    # Register agents
    graph.add_node("requirements", requirement_agent)
    graph.add_node("knowledge", knowledge_agent)
    graph.add_node("planner", planner_agent)
    graph.add_node("architecture", architecture_agent)
    graph.add_node("code_generator", code_generator_agent)
    graph.add_node("mcp_tools", mcp_tools_agent)
    graph.add_node("validator", validator_agent)

    # Define execution order
    graph.add_edge(START, "requirements")
    graph.add_edge("requirements", "knowledge")
    graph.add_edge("knowledge", "planner")
    graph.add_edge("planner", "architecture")
    graph.add_edge("architecture", "code_generator")
    graph.add_edge("code_generator", "mcp_tools")
    graph.add_edge("mcp_tools", "validator")
    graph.add_edge("validator", END)

    return graph.compile()


aegis_graph = build_graph()
