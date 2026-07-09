from app.ai.chains import travel_chain


class ChatService:

    @staticmethod
    async def chat(message: str) -> str:
        """
        AI聊天
        """

        reply = await travel_chain.ainvoke(
            {
                "question": message
            }
        )

        return reply