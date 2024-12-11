import json
from langchain_core.messages import (
    FunctionMessage,
    HumanMessage,
)
from langgraph.prebuilt.tool_executor import ToolExecutor, ToolInvocation
from tools import tools


# Tool Node Function
def tool_node(state):
    """
    Executes the tool based on the last message in the state and returns the tool's result.
    
    Args:
    - state: The current state, which contains the messages and other information.
    
    Returns:
    - A dictionary containing the result from the tool execution, formatted as a message.
    """
    messages = state["messages"]
    # Based on the continue condition
    # we know the last message involves a function call
    last_message = messages[-1]
    # We construct an ToolInvocation from the function_call
    tool_input = json.loads(
        last_message.additional_kwargs["function_call"]["arguments"]
    )
    # We can pass single-arg inputs by value
    if len(tool_input) == 1 and "__arg1" in tool_input:
        tool_input = next(iter(tool_input.values()))
    tool_name = last_message.additional_kwargs["function_call"]["name"]
    action = ToolInvocation(
        tool=tool_name,
        tool_input=tool_input,
    )
    # We call the tool_executor and get back a response
    tool_executor = ToolExecutor(tools)
    response = tool_executor.invoke(action)
    # We use the response to create a FunctionMessage
    function_message = FunctionMessage(
        content=f"{tool_name} response: {str(response)}", name=action.tool
    )
    # We return a list, because this will get added to the existing list
    return {"messages": [function_message]}

# Router Logic
def router(state):
    """
    Determines the next step based on the content of the last message in the state.
    
    Args:
    - state: The current state of the workflow.
    
    Returns:
    - A string representing the next step in the workflow, such as "continue", "call_tool", or "end".
    """
    # This is the router
    messages = state["messages"]
    last_message = messages[-1]
    if "function_call" in last_message.additional_kwargs:
        # The previus agent is invoking a tool
        return "call_tool"
    if "FINAL ANSWER" in last_message.content:
        # Any agent decided the work is done
        return "end"
    return "continue"


# Agent Node Execution
def agent_node(state, agent, name):
    """
    Executes an agent's action and updates the state with the agent's response.
    
    Args:
    - state: The current state of the workflow.
    - agent: The agent to invoke.
    - name: The name of the agent.
    
    Returns:
    - A dictionary containing the updated state with the agent's message.
    """
    result = agent.invoke(state)
    # We convert the agent output into a format that is suitable to append to the global state
    if isinstance(result, FunctionMessage):
        pass
    else:
        result = HumanMessage(**result.dict(exclude={"type", "name"}), name=name)
    return {
        "messages": [result],
        # Since we have a strict workflow, we can
        # track the sender so we know who to pass to next.
        "sender": name,
    }

