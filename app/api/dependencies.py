from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db_session
from app.repositories.user import UserRepository
from app.services.auth import AuthService
from app.services.post import PostService
from app.services.user import UserService


def get_post_service() -> PostService:
    return PostService()


PostServiceDep = Annotated[
    PostService,
    Depends(get_post_service),
]
DbSessionDep = Annotated[
    AsyncSession,
    Depends(get_db_session),
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


def get_auth_service(
    session: DbSessionDep,
    repository: UserRepositoryDep,
    user_service: UserServiceDep,
) -> AuthService:
    return AuthService(
        session=session,
        repository=repository,
        user_service=user_service,
    )


AuthServiceDep = Annotated[
    AuthService,
    Depends(get_auth_service),
]
