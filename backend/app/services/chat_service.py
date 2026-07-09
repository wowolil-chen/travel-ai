class ChatService:

    @staticmethod
    async def chat(message: str) -> str:
        """
        AI聊天
        """

        return f"收到你的问题：{message}，这是模拟回复。"