from langchain.agents import create_agent
from src.llm.qwen import get_llm
from src.tools.web_search import web_search

def create_react_agent():
    llm = get_llm()
    tools = [web_search]

    agent = create_agent(
        model=llm,
        tools=tools
    )

    return agent
