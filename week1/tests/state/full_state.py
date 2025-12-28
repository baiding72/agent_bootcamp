import sys
import os
from langchain.messages import HumanMessage
from src.llm.qwen import get_llm
from src.tools.web_search import web_search

def test_full_context():
    print("\n--- 实验 1: 完整上下文 (标准 ReAct) ---")
    llm = get_llm()
    tools = [web_search]
    
    # 1. 初始化对话历史
    query = "苹果 17 是什么时候发布的？"
    messages = [HumanMessage(content=query)]
    
    print(f"User: {query}")

    # --- 第一轮：LLM 思考与行动 (Thinking & Tool Call) ---
    # 绑定工具让 LLM 知道它可以调用
    llm_with_tools = llm.bind_tools(tools)
    ai_msg_1 = llm_with_tools.invoke(messages)
    
    print(f"\n[Step 1 LLM Output]: {ai_msg_1.content}")
    print(f"[Tool Calls]: {ai_msg_1.tool_calls}")

    # 关键点：将 LLM 的回复完整加入历史
    messages.append(ai_msg_1) 

    # --- 第二轮：工具执行 (Tool Result) ---
    if ai_msg_1.tool_calls:
        for tool_call in ai_msg_1.tool_calls:
            tool_name = tool_call["name"]
            tool_args = tool_call["args"]
            
            print(f"\n[System]: Calling tool {tool_name}...")
            tool_result = tools[0].invoke(tool_args)
            
            # 构造工具回传消息
            from langchain_core.messages import ToolMessage
            tool_msg = ToolMessage(content=str(tool_result), tool_call_id=tool_call["id"])
            
            # 关键点：将工具结果加入历史
            messages.append(tool_msg)
            print(f"[Tool Result]: {str(tool_result)[:100]}...") # 只打印前100字

    # --- 第三轮：最终回答 (Final Answer) ---
    print("\n[System]: Sending full history back to LLM...")
    final_response = llm_with_tools.invoke(messages)
    print(f"\n[Final Answer]: {final_response.content}")

if __name__ == "__main__":
    test_full_context()