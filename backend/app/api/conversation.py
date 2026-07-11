from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.security import get_current_user
from app.db.session import get_db
from app.models.user import User
from app.schemas.conversation import (
    ConversationCreate,
    ConversationResponse,
)
from app.schemas.message import MessageResponse
from app.services.conversation_service import ConversationService
from app.services.message_service import MessageService

router = APIRouter(
    prefix="/api/conversations",
    tags=["Conversation"],
)


@router.post(
    "",
    response_model=ConversationResponse,
)
def create_conversation(
    data: ConversationCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return ConversationService.create(
        db=db,
        user_id=current_user.id,
        title=data.title,
    )


@router.get(
    "",
    response_model=list[ConversationResponse],
)
def get_conversations(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return ConversationService.get_list(
        db=db,
        user_id=current_user.id,
    )


@router.get(
    "/{conversation_id}/messages",
    response_model=list[MessageResponse],
)
def get_messages(
    conversation_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    conversation = ConversationService.get_by_id(
        db=db,
        conversation_id=conversation_id,
        user_id=current_user.id,
    )

    if conversation is None:
        raise HTTPException(
            status_code=404,
            detail="会话不存在",
        )

    return MessageService.get_messages(
        db=db,
        conversation_id=conversation_id,
    )


@router.delete("/{conversation_id}")
def delete_conversation(
    conversation_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    conversation = ConversationService.get_by_id(
        db=db,
        conversation_id=conversation_id,
        user_id=current_user.id,
    )

    if conversation is None:
        raise HTTPException(
            status_code=404,
            detail="会话不存在",
        )

    ConversationService.delete(
        db=db,
        conversation=conversation,
    )

    return {
        "message": "删除成功"
    }