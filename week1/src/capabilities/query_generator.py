from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from src.llm.qwen import get_llm

QUERY_PROMPT = """你是一个搜索查询生成器。

你的任务是：
- 将用户问题转化为适合搜索引擎的关键词
- 简短、具体、避免口语
- 不要回答问题本身

只输出搜索查询字符串。

用户问题：
{question}
"""

def generate_search_query(question: str) -> str:
    llm = get_llm()

    prompt = PromptTemplate.from_template(QUERY_PROMPT)
    parser = StrOutputParser()

    runnable = prompt | llm | parser
    return runnable.invoke({"question": question})
