import os
import json
from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain_classic.agents import create_tool_calling_agent, AgentExecutor
from langchain_core.messages import HumanMessage, AIMessage
from langchain_community.tools.tavily_search import TavilySearchResults

from models import UserProfile
from memory.profile_manager import UserProfileManager
from prompts.persona import get_chat_prompt, get_extraction_components

load_dotenv()

# --- 1. 初始化 ---
llm = ChatOpenAI(model="qwen-plus", 
                 openai_api_key=os.getenv("QWEN_API_KEY"),
                 openai_api_base=os.getenv("QWEN_BASE_URL"),
                 temperature=0) # 提取信息时温度要低
tools = [TavilySearchResults(max_results=1)]
profile_manager = UserProfileManager()

# --- 2. 构建 Chat Agent (Runnable) ---
# create_tool_calling_agent 本身返回的就是一个 Runnable，不是 Chain 类
agent_runnable = create_tool_calling_agent(llm, tools, get_chat_prompt())
# AgentExecutor 是目前唯一的运行时封装 (LangGraph 是下一代替代品，但 Week 2 暂不引入)
agent_executor = AgentExecutor(agent=agent_runnable, tools=tools, verbose=True)

# --- 3. 构建记忆提取管道 (Pure LCEL) ---
# 获取 prompt 和 parser
extract_prompt, extract_parser = get_extraction_components()

# 【核心修改】：使用管道符 | 构建 Runnable
# Input -> Prompt -> LLM -> Parser -> Structure Object
extraction_runnable = extract_prompt | llm | extract_parser

def run_chat_loop():
    print("🐱 赛博喵 (LCEL版) 启动... (输入 'exit' 退出)")
    chat_history = []
    
    while True:
        user_input = input("\nUser: ")
        if user_input.lower() == "exit": break
            
        # A. 读档
        current_profile_dict = profile_manager.load_profile()
        # 转换成字符串喂给 Chat Agent
        profile_str = json.dumps(current_profile_dict, ensure_ascii=False)
        
        # B. 聊天 (Chat Loop)
        response = agent_executor.invoke({
            "input": user_input,
            "chat_history": chat_history,
            "user_profile": profile_str
        })
        ai_content = response["output"]
        print(f"CyberNeko: {ai_content}")
        
        # C. 记忆提取 (Sidecar Extraction)
        # 直接调用 LCEL Runnable，它会自动返回 UserProfile 对象，无需 json.loads
        try:
            print("\n[系统后台] 正在提取记忆 (LCEL Pipeline)...")
            extracted_profile: UserProfile = extraction_runnable.invoke({
                "input": user_input,
                "ai_response": ai_content
            })
            
            # D. 存档
            # 只有当提取出的对象里有实质内容时才更新
            if any(value for value in extracted_profile.model_dump().values()):
                new_data = profile_manager.update_profile(extracted_profile)
                print(f"[记忆更新] 成功合并: {extracted_profile.model_dump(exclude_none=True)}")
            else:
                print("[记忆更新] 未发现新信息")
                
        except Exception as e:
            print(f"[系统错误] {e}")

        # 更新短期历史
        chat_history.append(HumanMessage(content=user_input))
        chat_history.append(AIMessage(content=ai_content))

if __name__ == "__main__":
    run_chat_loop()