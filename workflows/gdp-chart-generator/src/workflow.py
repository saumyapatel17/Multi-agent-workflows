import functools
import operator
from typing import Annotated, Sequence, TypedDict
from typing_extensions import TypedDict
from langgraph.graph import END, StateGraph
from langchain_core.messages import BaseMessage
from utils import agent_node, tool_node, router
from agents import research_agent, chart_agent

# Define Agent State Structure
class AgentState(TypedDict):
    """
    Defines the structure of the state that will be passed between different nodes in the workflow.
    It includes the messages exchanged and the sender of each message.
    
    Attributes:
    - messages: A sequence of messages exchanged between agents.
    - sender: The name of the agent who sent the message.
    """
    messages: Annotated[Sequence[BaseMessage], operator.add]
    sender: str

# Workflow Creation
research_node = functools.partial(agent_node, agent=research_agent, name="Researcher")
chart_node = functools.partial(agent_node, agent=chart_agent, name="Chart Generator")

# Building the Graph
workflow = StateGraph(AgentState)
workflow.add_node("Researcher", research_node)
workflow.add_node("Chart Generator", chart_node)
workflow.add_node("call_tool", tool_node)

# Define Conditional Edges hat will route messages as per the conditions fulfilled
workflow.add_conditional_edges(
    "Researcher", router, {"continue": "Chart Generator", "call_tool": "call_tool", "end": END}
)
workflow.add_conditional_edges(
    "Chart Generator", router, {"continue": "Researcher", "call_tool": "call_tool", "end": END}
)
workflow.add_conditional_edges(
    "call_tool",
    lambda x: x["sender"],
    {"Researcher": "Researcher", "Chart Generator": "Chart Generator"},
)

# Set Entry Point and Compile Graph
workflow.set_entry_point("Researcher")
graph = workflow.compile()