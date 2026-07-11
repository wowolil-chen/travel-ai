from datetime import datetime

from sqlalchemy.orm import Session

from app.models.conversation import Conversation


class ConversationService:
    """
    会话业务
    """

    @staticmethod
    def create(
        db: Session,
        user_id: int,
        title: str = "新对话",
    ) -> Conversation:
        """
        创建会话
        """

        conversation = Conversation(
            user_id=user_id,
            title=title,
        )

        db.add(conversation)
        db.commit()
        db.refresh(conversation)

        return conversation

    @staticmethod
    def get_list(
        db: Session,
        user_id: int,
    ) -> list[Conversation]:
        """
        获取当前用户所有会话
        """

        return (
            db.query(Conversation)
            .filter(Conversation.user_id == user_id)
            .order_by(Conversation.updated_at.desc())
            .all()
        )

    @staticmethod
    def get_by_id(
        db: Session,
        conversation_id: int,
        user_id: int,
    ) -> Conversation | None:
        """
        根据ID获取会话
        """

        return (
            db.query(Conversation)
            .filter(
                Conversation.id == conversation_id,
                Conversation.user_id == user_id,
            )
            .first()
        )

    @staticmethod
    def update_title(
        db: Session,
        conversation: Conversation,
        title: str,
    ) -> Conversation:
        """
        更新会话标题
        """

        conversation.title = title

        db.commit()
        db.refresh(conversation)

        return conversation

    @staticmethod
    def touch(
        db: Session,
        conversation: Conversation,
    ) -> Conversation:
        """
        更新会话最后更新时间
        """

        conversation.updated_at = datetime.now()

        db.commit()
        db.refresh(conversation)

        return conversation

    @staticmethod
    def delete(
        db: Session,
        conversation: Conversation,
    ) -> None:
        """
        删除会话
        """

        db.delete(conversation)
        db.commit()