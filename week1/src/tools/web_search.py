from dotenv import load_dotenv
from tavily import TavilyClient
from langchain.tools import tool
import os

load_dotenv()


def _get_tavily_client() -> TavilyClient:
    api_key = os.getenv("TAVILY_API_KEY")
    if not api_key:
        raise RuntimeError("TAVILY_API_KEY not found in environment")
    return TavilyClient(api_key=api_key)


@tool
def web_search(query: str) -> str:
    """
    使用搜索引擎搜索互联网信息。
    输入应该是一个简洁的搜索关键词或问题。
    """
    client = _get_tavily_client()

    response = client.search(
        query=query,
        search_depth="basic",   # basic / advanced
        max_results=5,
    )

    results = response.get("results", [])
    if not results:
        return "未搜索到相关信息。"

    # 把搜索结果整理成 Agent 友好的文本
    formatted_results = []
    for i, item in enumerate(results, start=1):
        title = item.get("title", "")
        content = item.get("content", "")
        url = item.get("url", "")
        formatted_results.append(
            f"{i}. {title}\n{content}\n来源: {url}"
        )

    return "\n\n".join(formatted_results)
