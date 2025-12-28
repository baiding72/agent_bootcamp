from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import PydanticOutputParser
from models import UserProfile

# --- 1. 聊天主 Prompt (保持不变) ---
CHAT_SYSTEM_TEMPLATE = """
你叫“赛博喵(CyberNeko)”，一个来自 2077 年的傲娇 AI 助手。
说话风格：句尾加“喵~”，有点毒舌但很靠谱。
【当前用户档案】：
{user_profile}
"""

def get_chat_prompt():
    return ChatPromptTemplate.from_messages([
        ("system", CHAT_SYSTEM_TEMPLATE),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ])

# --- 2. 记忆提取 Prompt (重构为 LCEL 风格) ---
EXTRACTION_SYSTEM_TEMPLATE = """
你是一个侧写师。请从下方的对话中提取用户的信息。
如果对话中没有包含某项信息，请保持字段为 null 或空列表。

{format_instructions}

不要输出任何多余的解释，只输出 JSON。
"""

def get_extraction_components():
    """
    返回 LCEL 所需的 prompt 和 parser
    """
    # 实例化解析器 (这就相当于 Jackson/Gson)
    parser = PydanticOutputParser(pydantic_object=UserProfile)
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", EXTRACTION_SYSTEM_TEMPLATE),
        ("human", "对话内容：\nUser: {input}\nAI: {ai_response}")
    ])
    
    # 将解析器的 schema 说明注入到 prompt 中
    prompt = prompt.partial(format_instructions=parser.get_format_instructions())
    
    return prompt, parser