from fastapi import HTTPException
from langchain_core.messages import (
    AIMessage,
    HumanMessage,
)

from sqlalchemy.orm import Session

from app.ai.agent import chat_with_tools
from app.models.user import User
from app.services.conversation_service import ConversationService
from app.services.message_service import MessageService


class ChatService:
    """
    AI 聊天业务
    """

    @staticmethod
    async def chat_stream(
        db: Session,
        current_user: User,
        conversation_id: int,
        message: str,
    ):
        """
        流式聊天
        """

        # 查询会话
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

        # 首次聊天自动生成标题
        if conversation.title == "新对话":
            ConversationService.update_title(
                db=db,
                conversation=conversation,
                title=message[:20],
            )

        # 保存用户消息
        MessageService.create(
            db=db,
            conversation_id=conversation_id,
            role="user",
            content=message,
        )

        # 获取历史消息
        history = MessageService.get_messages(
            db=db,
            conversation_id=conversation_id,
        )

        # 构建 LangChain Messages
        messages = []

        for item in history:

            if item.role == "user":
                messages.append(
                    HumanMessage(
                        content=item.content,
                    )
                )

            elif item.role == "assistant":
                messages.append(
                    AIMessage(
                        content=item.content,
                    )
                )

        full_reply = ""

        try:

            async for chunk in chat_with_tools(messages):

                full_reply += chunk

                yield chunk

            # 保存 AI 回复
            if full_reply.strip():

                MessageService.create(
                    db=db,
                    conversation_id=conversation_id,
                    role="assistant",
                    content=full_reply,
                )

                ConversationService.touch(
                    db=db,
                    conversation=conversation,
                )

        except Exception as e:

            yield f"\n\n[ERROR] {str(e)}"