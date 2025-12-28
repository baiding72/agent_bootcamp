from langchain.tools import tool

@tool
def web_search(query: str) -> str:
    """
    使用搜索引擎搜索信息
    """
    # Week 1 先 mock，后面再接真实 API
    return f"搜索结果（模拟）：关于 {query} 的一些网页信息..."
