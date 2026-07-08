from pydantic import BaseModel, Field


class UserLogin(BaseModel):
    """
    登录请求
    """

    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=6, max_length=20)


class UserCreate(BaseModel):
    """
    注册请求
    """

    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=6, max_length=20)
    nickname: str | None = None


class UserResponse(BaseModel):
    """
    返回用户信息
    """

    id: int
    username: str
    nickname: str | None

    model_config = {
        "from_attributes": True
    }