from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

from app.core.security import get_current_user
from app.db.session import get_db
from app.models.user import User
from app.schemas.chat import ChatRequest
from app.services.chat_service import ChatService

router = APIRouter(
    prefix="/api/chat",
    tags=["Chat"],
)


@router.post("")
async def chat(
    data: ChatRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    AI 流式聊天
    """

    return StreamingResponse(
        ChatService.chat_stream(
            db=db,
            current_user=current_user,
            conversation_id=data.conversation_id,
            message=data.message,
        ),
        media_type="text/plain",
    )