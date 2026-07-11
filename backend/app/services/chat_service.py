from fastapi import HTTPException
from langchain_core.messages import (
    SystemMessage,
    HumanMessage,
    AIMessage,
)
from sqlalchemy.orm import Session

from app.ai.model import llm
from app.models.user import User
from app.services.conversation_service import ConversationService
from app.services.message_service import MessageService


SYSTEM_PROMPT = """
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
"""


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

        # 获取全部历史记录
        history = MessageService.get_messages(
            db=db,
            conversation_id=conversation_id,
        )

        # 构建 LangChain Messages
        messages = [
            SystemMessage(
                content=SYSTEM_PROMPT
            )
        ]

        for item in history:

            if item.role == "user":
                messages.append(
                    HumanMessage(
                        content=item.content
                    )
                )

            elif item.role == "assistant":
                messages.append(
                    AIMessage(
                        content=item.content
                    )
                )

        full_reply = ""

        try:

            # LangChain Streaming
            async for chunk in llm.astream(messages):

                if not chunk.content:
                    continue

                full_reply += chunk.content

                # 实时返回给前端
                yield chunk.content

            # 保存 AI 回复
            if full_reply.strip():

                MessageService.create(
                    db=db,
                    conversation_id=conversation_id,
                    role="assistant",
                    content=full_reply,
                )

                # 更新会话时间
                ConversationService.touch(
                    db=db,
                    conversation=conversation,
                )

        except Exception as e:

            yield f"\n\n[ERROR] {str(e)}"