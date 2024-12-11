import os
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_experimental.utilities import PythonREPL
from langchain_core.tools import tool
from typing import Annotated

# Set API keys for Tavily 
TAVILY_API_KEY = os.getenv('TAVILY_API_KEY', '<Your Default Tavily API Key>')

tavily_tool = TavilySearchResults(max_results=5) # Tavily Search Tool
repl = PythonREPL() # Python Tool (REPL)

@tool
def python_repl(code: Annotated[str, "The python code to execute to generate your chart."]):
    """
    Executes the provided Python code and returns the result. 
    This tool runs Python code and outputs the result, 
    which is useful for generating charts or performing calculations.

    Args:
    - code: A string containing the Python code to be executed.

    Returns:
    - A message indicating success or failure of execution, along with the result or error.
    """
    try:
        result = repl.run(code)
    except BaseException as e:
        return f"Failed to execute. Error: {repr(e)}"
    return f"Succesfully executed:\\\\n`python\\\\\\\\n{code}\\\\\\\\n`\\\\nStdout: {result}"

tools = [tavily_tool, python_repl]  
