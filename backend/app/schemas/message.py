from datetime import datetime

from pydantic import BaseModel


class MessageResponse(BaseModel):
    """
    聊天消息
    """

    id: int

    role: str

    content: str

    created_at: datetime

    model_config = {
        "from_attributes": True,
    }