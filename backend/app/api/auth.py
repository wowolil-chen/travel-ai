from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Request,
    status,
)
from sqlalchemy.orm import Session

from app.core.security import create_access_token
from app.db.session import get_db
from app.schemas.token import Token
from app.schemas.user import (
    UserCreate,
    UserLogin,
    UserResponse,
)
from app.services.user_service import UserService

router = APIRouter(
    prefix="/api/auth",
    tags=["Authentication"],
)


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
def register(
    user_data: UserCreate,
    db: Session = Depends(get_db),
):
    """
    用户注册
    """

    # 用户名已存在
    if UserService.get_by_username(
        db,
        user_data.username,
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="用户名已存在",
        )

    # 创建用户
    user = UserService.create(
        db=db,
        user_data=user_data,
    )

    return user


@router.post(
    "/login",
    response_model=Token,
)
def login(
    request: Request,
    user_data: UserLogin,
    db: Session = Depends(get_db),
):
    """
    用户登录
    """

    # 用户认证
    user = UserService.authenticate(
        db=db,
        username=user_data.username,
        password=user_data.password,
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户名或密码错误",
        )

    # 获取客户端 IP
    client_ip = request.headers.get("X-Forwarded-For")

    if client_ip:
        client_ip = client_ip.split(",")[0].strip()
    else:
        client_ip = request.client.host

    # 更新登录信息
    UserService.update_login_ip(
        db=db,
        user=user,
        ip=client_ip,
    )

    # 生成 JWT
    access_token = create_access_token(
        data={
            "user_id": user.id,
        }
    )

    # 返回 Token + 用户信息
    return Token(
        access_token=access_token,
        token_type="bearer",
        user=UserResponse.model_validate(user),
    )