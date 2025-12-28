from src.agent.react_agent import create_react_agent
from src.capabilities.query_generator import generate_search_query

def main():
    agent = create_react_agent()

    while True:
        question = input(">>> ")
        if question.lower() in ["exit", "quit"]:
            break

        question = generate_search_query(question)
        result = agent.invoke(
            {"messages": [{"role": "user", "content": question}]},
        )
        answer = result["messages"][-1].content
        print(answer)

if __name__ == "__main__":
    main()
