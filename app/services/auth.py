import asyncio
from datetime import UTC, datetime, timedelta

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import get_settings
from app.core.security import (
    DUMMY_PASSWORD_HASH,
    TokenPair,
    create_access_token,
    generate_refresh_token,
    hash_password,
    hash_refresh_token,
    verify_password,
)
from app.exceptions.auth import InvalidCredentialsError
from app.exceptions.user import UserAlreadyExistsError, UserNotFoundError
from app.models.enums import UserStatus
from app.models.user import User
from app.repositories.refresh_token import RefreshTokenRepository
from app.repositories.user import UserRepository
from app.schemas.user import UserCreate
from app.services.user import UserService


class AuthService:
    def __init__(
        self,
        session: AsyncSession,
        repository: UserRepository,
        refresh_token_repository: RefreshTokenRepository,
        user_service: UserService,
    ) -> None:
        self.session = session
        self.repository = repository
        self.user_service = user_service
        self.refresh_token_repository = refresh_token_repository

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

    async def login(self, email: str, password: str) -> TokenPair:
        settings = get_settings()

        async with self.session.begin():
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

            refresh_token = generate_refresh_token()
            expires_at = datetime.now(UTC) + timedelta(
                days=settings.refresh_token_expire_days,
            )

            await self.refresh_token_repository.create(
                user_id=user.id,
                token_hash=hash_refresh_token(refresh_token),
                expires_at=expires_at,
            )

            access_token = create_access_token(str(user.id))

        return TokenPair(access_token=access_token, refresh_token=refresh_token)

    async def refresh(self, refresh_token: str) -> TokenPair:
        token_hash = hash_refresh_token(refresh_token)

        stored_token = await self.refresh_token_repository.get_by_hash(token_hash)

        if stored_token is None:
            raise InvalidCredentialsError()

        if stored_token.revoked_at is not None:
            raise InvalidCredentialsError()

        now = datetime.now(UTC)

        if stored_token.expires_at <= now:
            raise InvalidCredentialsError()

        try:
            user = await self.user_service.get_user(stored_token.user_id)
        except UserNotFoundError:
            raise InvalidCredentialsError() from None

        if user.status != UserStatus.ACTIVE:
            raise InvalidCredentialsError()

        access_token = create_access_token(str(user.id))

        return TokenPair(access_token=access_token, refresh_token=refresh_token)

    async def logout(self, refresh_token: str) -> None:
        token_hash = hash_refresh_token(refresh_token)

        async with self.session.begin():
            await self.refresh_token_repository.revoke_by_hash(token_hash)
