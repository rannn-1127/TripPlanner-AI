from app.agent.agent import get_trip_agent


if __name__ == "__main__":
    agent = get_trip_agent()

    result = agent.invoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": "我准备去上海旅游3天，喜欢历史文化和夜景，旅行节奏比较休闲，请帮我规划行程。"
                }
            ]
        }
    )

    print("\n" + "=" * 60)
    print("最终行程")
    print("=" * 60)

    print(result["messages"][-1].content)