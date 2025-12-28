import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

from langchain_core.messages import HumanMessage, ToolMessage, AIMessage
from src.llm.qwen import get_llm
from src.tools.web_search import web_search



def test_drop_tool_call():
    print("\n--- 实验 3: 缺失 Tool Call (凭空出现的记忆) ---")
    llm = get_llm()
    tools = [web_search]
    llm_with_tools = llm.bind_tools(tools)
    
    query = "马斯克最近有什么新闻？"
    
    # 1. 正常生成 Tool Call
    ai_msg_original = llm_with_tools.invoke([HumanMessage(content=query)])
    tool_call = ai_msg_original.tool_calls[0]
    
    # 2. 执行工具获取结果
    tool_res = tools[0].invoke(tool_call["args"])
    tool_msg = ToolMessage(content=str(tool_res), tool_call_id=tool_call["id"])
    
    # 3. 构建"被篡改"的历史
    # 我们故意跳过了 ai_msg_original，直接把 tool_msg 塞给 LLM
    # 历史变成了: [User, ToolResult]
    # 注意: 大部分 LLM API 会因为 ID 不匹配报错，所以我们这里模拟一种"逻辑缺失"
    # 我们塞入一个普通的 AI 回复，假装它没调用工具，但结果却出现了
    
    corrupted_messages = [
        HumanMessage(content=query),
        # 这一行本该包含 tool_calls，但我们把它替换成了普通废话
        AIMessage(content="好的，让我想想..."), 
        tool_msg
    ]
    
    print(f"\n[Context Sent to LLM]: \n1. User: {query} \n2. AI: 好的... \n3. Tool Output: {str(tool_res)[:50]}...")
    
    try:
        print("\n[System]: Invoking LLM with corrupted context...")
        response = llm_with_tools.invoke(corrupted_messages)
        print(f"\n[Resulting Behavior]: {response.content}")
        print(">> 分析: LLM 可能会感到困惑，'我没查这个，为什么会有搜索结果？'，或者它会忽略这个结果重新搜索。")
    except Exception as e:
        print(f"\n[API Error]: {e}")
        print(">> 分析: 现代 LLM API (如 OpenAI) 强制检查上下文连贯性。缺失 Tool Call 会导致 'Orphaned Tool Output' 错误。这证明了上下文完整性的重要性。")

if __name__ == "__main__":
    test_drop_tool_call()