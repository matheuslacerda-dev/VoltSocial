from collections.abc import Awaitable, Callable
from typing import Annotated

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.permissions import Permission, has_permission
from app.core.security import decode_access_token
from app.db.session import get_db_session
from app.exceptions.user import UserNotFoundError
from app.models.enums import UserStatus
from app.models.user import User
from app.repositories.refresh_token import RefreshTokenRepository
from app.repositories.user import UserRepository
from app.services.auth import AuthService
from app.services.post import PostService
from app.services.user import UserService

bearer_scheme = HTTPBearer(auto_error=False)

DbSessionDep = Annotated[
    AsyncSession,
    Depends(get_db_session),
]


def get_post_service() -> PostService:
    return PostService()


PostServiceDep = Annotated[
    PostService,
    Depends(get_post_service),
]


def get_user_repository(
    session: DbSessionDep,
) -> UserRepository:
    return UserRepository(session)


UserRepositoryDep = Annotated[
    UserRepository,
    Depends(get_user_repository),
]


def get_user_service(repository: UserRepositoryDep) -> UserService:
    return UserService(repository)


UserServiceDep = Annotated[
    UserService,
    Depends(get_user_service),
]


def _unauthorized() -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials.",
        headers={"WWW-Authenticate": "Bearer"},
    )


async def get_current_user(
    credentials: Annotated[
        HTTPAuthorizationCredentials | None,
        Depends(bearer_scheme),
    ],
    user_service: UserServiceDep,
) -> User:
    if credentials is None:
        raise _unauthorized()

    try:
        subject = decode_access_token(credentials.credentials)
        user_id = int(subject)
    except (jwt.InvalidTokenError, ValueError):
        raise _unauthorized() from None

    try:
        user = await user_service.get_user(user_id)
    except UserNotFoundError:
        raise _unauthorized() from None

    if user.status != UserStatus.ACTIVE:
        raise _unauthorized()

    return user


CurrentUserDep = Annotated[
    User,
    Depends(get_current_user),
]


def get_refresh_token_repository(
    session: DbSessionDep,
) -> RefreshTokenRepository:
    return RefreshTokenRepository(session)


RefreshTokenRepositoryDep = Annotated[
    RefreshTokenRepository,
    Depends(get_refresh_token_repository),
]


def get_auth_service(
    session: DbSessionDep,
    repository: UserRepositoryDep,
    refresh_token_repository: RefreshTokenRepositoryDep,
    user_service: UserServiceDep,
) -> AuthService:
    return AuthService(
        session=session,
        repository=repository,
        refresh_token_repository=refresh_token_repository,
        user_service=user_service,
    )


AuthServiceDep = Annotated[
    AuthService,
    Depends(get_auth_service),
]


def require_permission(
    permission: Permission,
) -> Callable[..., Awaitable[User]]:
    async def checker(current_user: CurrentUserDep) -> User:
        if not has_permission(current_user.role, permission):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to perform this action.",
            )
        return current_user

    return checker
