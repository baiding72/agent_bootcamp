from langchain.messages import AIMessage

def drop_thinking(messages):
    return [
        m for m in messages
        if not (
            isinstance(m, AIMessage)
            and "Thought:" in m.get("content", "")
        )
    ]
