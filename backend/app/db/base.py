from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


# 导入所有模型，让 SQLAlchemy 注册
import app.models.user
import app.models.conversation
import app.models.message