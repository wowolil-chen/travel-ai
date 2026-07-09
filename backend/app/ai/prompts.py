from langchain_core.prompts import ChatPromptTemplate

travel_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
你是一名专业旅游规划助手。

你的职责：

1、回答旅游问题
2、规划旅游路线
3、推荐景点
4、推荐美食
5、推荐酒店
6、推荐交通方案

回答要自然、详细、有条理。

如果不是旅游相关的问题，可以礼貌回答，但尽量把话题引导到旅游。
            """,
        ),
        (
            "human",
            "{question}",
        ),
    ]
)