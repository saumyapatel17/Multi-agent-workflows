# GDP Chart Generator with Multi-Agent System

This project uses **Langchain** and **Langgraph** to create a multi-agent workflow. The system fetches the GDP data of Malaysia over the past five years and generates a chart based on that data using a multi-agent architecture.

## Requirements

### Python Version:
- Python 3.10 or higher

### Install Dependencies:

```bash
pip install -r requirements.txt
```

## Setup

### Environment Variables

Create a `.env` file in the root directory of your project and add the following environment variables:

```bash
TAVILY_API_KEY=<Your Tavily API Key>
OPENAI_API_KEY=<Your OpenAI API Key>
```

### Dependencies

The project uses the following key dependencies:

- **Langchain**: For LLMs, agents, and tools.
- **Langgraph**: For building multi-agent workflows.
- **PythonREPL**: For executing Python code to generate charts, a tool to execute python code
- **Tavily Search API**: For retrieving external data, an Internet Search Tool

## How It Works

This system is built using a multi-agent framework where:

1. **Researcher Agent**: Fetches GDP data for Malaysia over the past 5 years.
2. **Chart Generator Agent**: Uses the fetched data to generate a line chart.
3. **Tool Executor**: Executes the tools (e.g., Python REPL for chart generation, Tavily Search for data retrieval).

The workflow orchestrates the agents and tools to solve the task.

## Running the Script

To execute the script and run the multi-agent workflow, use the following command:

```bash
python main.py
```

### Expected Output:

The system will prompt you to enter the task, which in this case is fetching GDP data for Malaysia and generating a chart. Once the process is complete, the output will include the final result (the generated chart) or any errors encountered during execution.

## Code Structure

The code is organized as follows:

1. **`tools.py`**: Defines the tools, such as the Tavily Search Tool and Python REPL, which are used in the agent tasks.
2. **`agents.py`**: Defines the agents, such as the Researcher and Chart Generator agents. These agents collaborate using the tools to fetch data and generate the chart.
3. **`main.py`**: The main entry point where the multi-agent workflow is defined, and the agents are executed in a sequence to complete the task.

## Example Workflow

1. **Researcher Agent**: 
   - Fetches GDP data over the last 5 years using the Tavily Search API.
   
2. **Chart Generator Agent**:
   - Generates a Python chart (line graph) based on the retrieved GDP data.

3. **Multi-Agent Routing**:
   - The agents communicate and pass messages between each other to complete the task. If the Researcher agent requires additional data or tool invocation, it uses the Tool Executor to run necessary tools.

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
