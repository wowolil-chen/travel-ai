from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    """
    聊天请求
    """

    conversation_id: int = Field(
        ...,
        description="会话ID",
    )

    message: str = Field(
        ...,
        min_length=1,
        max_length=2000,
        description="用户消息",
    )


class ChatResponse(BaseModel):
    """
    非流式返回（预留）
    """

    reply: str