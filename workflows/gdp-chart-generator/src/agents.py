import os
from langchain_openai import ChatOpenAI
from langchain_core.utils.function_calling import convert_to_openai_function
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from tools import tavily_tool, python_repl

# Set API keys for OpenAI
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', '<Your Default OpenAI API Key>')

# LLM Setup for Agents (using OpenAI)
llm = ChatOpenAI(api_key=OPENAI_API_KEY)

# Function to Create Agents
def create_agent(llm, tools, system_message: str):
    """
    Creates an agent with the provided tools and system message.
    
    Args:
    - llm: The language model used for the agent.
    - tools: A list of tools available to the agent.
    - system_message: A message to be passed to the agent during its setup.
    
    Returns:
    - The created agent configured with the provided tools and system message.
    """
    functions = [convert_to_openai_function(t) for t in tools]
    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "You are a helpful AI assistant, collaborating with other assistants."
                " Use the provided tools to progress towards answering the question."
                " If you are unable to fully answer, that's OK, another assistant with different tools "
                " will help where you left off. Execute what you can to make progress."
                " If you or any of the other assistants have the final answer or deliverable,"
                " prefix your response with FINAL ANSWER so the team knows to stop."
                " You have access to the following tools: {tool_names}.\\\\n{system_message}",
            ),
            MessagesPlaceholder(variable_name="messages"),
        ]
    )
    prompt = prompt.partial(system_message=system_message)
    prompt = prompt.partial(tool_names=", ".join([tool.name for tool in tools]))
    return prompt | llm.bind_functions(functions)

# Create Researcher and Chart Generator Agents
research_agent= create_agent(
    llm,
    [tavily_tool],
    system_message="You should provide accurate data for the chart generator to use.",
)

chart_agent= create_agent(
    llm,
    [python_repl],
    system_message="Any charts you display will be visible by the user.",
)
