from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
import os

load_dotenv()

def get_llm():
    return ChatOpenAI(
        model="qwen-plus",
        openai_api_key=os.getenv("QWEN_API_KEY"),
        openai_api_base=os.getenv("QWEN_BASE_URL"),
        temperature=0
    )
