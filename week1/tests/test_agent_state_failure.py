from typing import Callable, List
from langchain_core.messages import BaseMessage
from tests.state.full_state import build_agent
from tests.state.drop_thinking import drop_thinking
from tests.state.drop_tool_call import drop_tool_call
from tests.state.drop_tool_result import drop_tool_result

def run_experiment(
    agent,
    modifier: Callable[[List[BaseMessage]], List[BaseMessage]],
    question: str,
    title: str,
):
    print("\n" + "=" * 80)
    print(f"Experiment: {title}")
    print("=" * 80)

    # Initial AgentState
    state = {
        "messages": [{"role": "user", "content": question}]
    }

    # Run agent
    result = agent.invoke(state)

    original_messages = result["messages"]
    modified_messages = modifier(original_messages)

    # print("\n--- Original AgentState ---")
    # for m in original_messages:
    #     print(f"{type(m).__name__}: {m.content}")

    # print("\n--- Modified AgentState ---")
    # for m in modified_messages:
    #     print(f"{type(m).__name__}: {m.content}")
    # print("\nObservation:")
    # print(
    #     "- Message count:", len(original_messages),
    #     "->", len(modified_messages)
    # )
    print(modified_messages[-1].content)

if __name__ == "__main__":
    agent = build_agent()
    question = "厦门今天是否发布了暴雨红色预警？"

    # Control group (no modification)
    run_experiment(
        agent=agent,
        modifier=lambda x: x,
        question=question,
        title="FULL CONTEXT (Control Group)",
    )

    # Missing thinking
    run_experiment(
        agent=agent,
        modifier=drop_thinking,
        question=question,
        title="DROP THINKING (Black-box Behavior)",
    )

    # Missing tool call
    run_experiment(
        agent=agent,
        modifier=drop_tool_call,
        question=question,
        title="DROP TOOL CALL (Untraceable Actions)",
    )

    # Missing tool result
    run_experiment(
        agent=agent,
        modifier=drop_tool_result,
        question=question,
        title="DROP TOOL RESULT (Retry / Misplanning)",
    )