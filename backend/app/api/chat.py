from fastapi import APIRouter

from app.schemas.chat import ChatRequest, ChatResponse
from app.services.chat_service import ChatService

router = APIRouter(
    prefix="/api/chat",
    tags=["聊天"],
)


@router.post(
    "",
    response_model=ChatResponse,
)
async def chat(data: ChatRequest):

    reply = await ChatService.chat(
        data.message
    )

    return ChatResponse(
        reply=reply
    )