from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    """
    聊天请求
    """

    message: str = Field(
        ...,
        min_length=1,
        max_length=2000,
        description="用户输入内容"
    )


class ChatResponse(BaseModel):
    """
    聊天响应
    """

    reply: str