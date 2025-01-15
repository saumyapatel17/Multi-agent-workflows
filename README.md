# Multiagent Workflows

Welcome to the **Multiagent Workflows** repository! This repository showcases projects that demonstrate the power of multi-agent systems using advanced AI frameworks like **LlamaIndex** and **LangChain's LangGraph**. Multi-agent systems are composed of multiple specialized AI agents working collaboratively to solve complex tasks efficiently.

## Overview

### What are Multi-Agent Systems?
Multi-agent systems function like teams of specialized workers, each with unique expertise. These agents collaborate to accomplish intricate workflows that would be challenging for a single entity to handle alone. By leveraging frameworks like LangGraph, we can structure these agents into dynamic workflows where each agent contributes to the overall task.

### Key Concepts
- **Agents**: Independent actors powered by Large Language Models (LLMs), each with its own configuration.
- **Collaboration**: Agents share information using a common "scratchpad," enabling transparent communication.
- **LangGraph Framework**: A tool that structures agents as nodes in a graph, with edges representing communication and control conditions guiding data flow.

## Projects
This repository contains several projects that exemplify multi-agent workflows:

### 1. **Flashcard Generator with LlamaIndex**
   - **Description**: A system that generates high-quality Anki flashcards from any text input using a multi-agent approach.
   - **Features**:
     - Text analysis to extract key points.
     - Collaborative agent workflow to ensure card quality.
     - Easy-to-integrate output for Anki flashcards.
   - **Technologies**:
     - [LlamaIndex](https://llamaindex.ai/) for text parsing and analysis.
     - Multi-agent collaboration for quality assurance.

### 2. **Collaborative Multi-Agent Workflow**
   - **Description**: A more complex system featuring multiple agents, each with a specific role, working together on a shared task.
   - **Features**:
     - Dynamic agent connections modeled as a graph.
     - State management for tracking agent progress.
     - Conditional logic to guide task flow.
   - **Technologies**:
     - LangChain's LangGraph for graph-based agent design.
     - Flexible prompts and tools tailored to each agent.

## Getting Started

### Prerequisites
- Python 3.10+
- Install dependencies:
  ```bash
  pip install -r requirements.txt
  ```

### Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/multiagent-workflows.git
   cd multiagent-workflows
   ```
2. Set up your environment:
   ```bash
   python -m venv env
   source env/bin/activate  # On Windows, use `env\Scripts\activate`
   ```
3. Install required packages:
   ```bash
   pip install -r requirements.txt
   ```

## Usage
- Each project is in its own directory under the `projects/` folder.
- Follow the `README.md` in each project's folder for specific instructions on running the examples.

## Contributing
Contributions are welcome! Please follow these steps:
1. Fork the repository.
2. Create a new branch (`feature/your-feature-name`).
3. Commit your changes.
4. Push to the branch and submit a Pull Request.

## License
This repository is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgments
- [LangChain](https://www.langchain.com/) for the LangGraph framework.
- [LlamaIndex](https://llamaindex.ai/) for enabling advanced text analysis.

## Additional Resources
- [Building a Multi-Agent System using CrewAI](https://medium.com/pythoneers/building-a-multi-agent-system-using-crewai-a7305450253e)
- [Build Multi-Agent System](https://www.analyticsvidhya.com/blog/2024/09/build-multi-agent-system/)
- [Multi-Agent Workflows using LangGraph and Langchain](https://vijaykumarkartha.medium.com/multiple-ai-agents-creating-multi-agent-workflows-using-langgraph-and-langchain-0587406ec4e6)
- [Build Multi-Agent with LlamaIndex](https://dev.to/yukooshima/building-a-multi-agent-framework-from-scratch-with-llamaindex-5ecn)
---

Happy building with multi-agent workflows! 🚀
