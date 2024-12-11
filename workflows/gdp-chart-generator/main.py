from dotenv import load_dotenv  
from langchain_core.messages import HumanMessage
from src.workflow import graph

# Load environment variables from a .env file
load_dotenv()


for s in graph.stream(
    {
        "messages": [
            HumanMessage(
                content="Fetch the Malaysia's GDP over the past 5 years,"
                " then draw a line graph of it."
                " Once you code it up, finish."
            )
        ],
    },
    # Maximum number of steps to take in the graph
    {"recursion_limit": 150},
):
    print(s)
    print("----")