import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

from langchain_core.messages import HumanMessage
from src.llm.qwen import get_llm
from src.tools.web_search import web_search

def test_drop_tool_result():
    print("\n--- 实验 2: 缺失 Tool Result (健忘的聋子) ---")
    llm = get_llm()
    tools = [web_search]
    llm_with_tools = llm.bind_tools(tools)
    
    messages = [HumanMessage(content="今天的比特币价格是多少？")]
    
    # Step 1: LLM 决定搜索
    ai_msg_1 = llm_with_tools.invoke(messages)
    print(f"[LLM Decision]: {ai_msg_1.tool_calls}")
    messages.append(ai_msg_1) # 记住了自己要搜索

    # Step 2: 假装执行了工具，但是...
    # 我们故意 不把 ToolMessage append 到 messages 列表中！
    print("\n[System]: Tool executed, BUT result is DROPPED from memory.")
    
    # Step 3: 再次请求 LLM
    # 此时 LLM 看到的历史是: [User, AI(我要搜索)]
    # 它没看到结果，它会怎么做？
    print("\n[System]: Asking LLM again...")
    ai_msg_2 = llm_with_tools.invoke(messages)
    
    print(f"\n[Resulting Behavior]: {ai_msg_2.tool_calls if ai_msg_2.tool_calls else ai_msg_2.content}")
    
    if ai_msg_2.tool_calls:
        print(">> 分析: LLM 再次发起了相同的工具调用。因为它以为上一次没执行成功。这就是'无限重试'循环。")
    else:
        print(">> 分析: LLM 开始胡言乱语或抱怨没有收到结果。")

if __name__ == "__main__":
    test_drop_tool_result()