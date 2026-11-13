import asyncio

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import (
    DUMMY_PASSWORD_HASH,
    create_access_token,
    hash_password,
    verify_password,
)
from app.exceptions.auth import InvalidCredentialsError
from app.exceptions.user import UserAlreadyExistsError
from app.models.enums import UserStatus
from app.models.user import User
from app.repositories.user import UserRepository
from app.schemas.user import UserCreate
from app.services.user import UserService


class AuthService:
    def __init__(
        self,
        session: AsyncSession,
        repository: UserRepository,
        user_service: UserService,
    ) -> None:
        self.session = session
        self.repository = repository
        self.user_service = user_service

    async def register(self, data: UserCreate) -> User:
        password_hash = await asyncio.to_thread(
            hash_password,
            data.password,
        )

        try:
            async with self.session.begin():
                await self.user_service.ensure_identity_available(
                    username=data.username,
                    email=data.email,
                )
                user = User(
                    name=data.name,
                    username=data.username,
                    email=data.email,
                    password_hash=password_hash,
                )

                return await self.repository.create(user)
        except IntegrityError as exc:
            constraint_name = self._get_constraint_name(exc)

            if constraint_name == "ux_users_username_lower":
                raise UserAlreadyExistsError("username") from exc

            if constraint_name == "ux_users_email_lower":
                raise UserAlreadyExistsError("email") from exc

            raise

    @staticmethod
    def _get_constraint_name(exc: IntegrityError) -> str | None:
        original = exc.orig

        constraint_name = getattr(
            original,
            "constraint_name",
            None,
        )

        if constraint_name:
            return constraint_name

        diagnostic = getattr(original, "diag", None)

        return getattr(
            diagnostic,
            "constraint_name",
            None,
        )

    async def login(self, email: str, password: str) -> str:
        user = await self.repository.get_by_email(email)

        hashed = user.password_hash if user else DUMMY_PASSWORD_HASH

        password_ok = await asyncio.to_thread(
            verify_password,
            password,
            hashed,
        )

        if user is None or not password_ok:
            raise InvalidCredentialsError()

        if user.status != UserStatus.ACTIVE:
            raise InvalidCredentialsError()

        return create_access_token(str(user.id))
