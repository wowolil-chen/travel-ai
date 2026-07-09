import asyncio

from app.ai.chains import travel_chain


async def main():
    result = await travel_chain.ainvoke(
        {
            "question": "我想去广州玩三天，请帮我规划行程。"
        }
    )

    print(result)


if __name__ == "__main__":
    asyncio.run(main())