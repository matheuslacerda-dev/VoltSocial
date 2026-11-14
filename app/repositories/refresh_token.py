from datetime import UTC, datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.refresh_token import RefreshToken


class RefreshTokenRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create(
        self,
        user_id: int,
        token_hash: str,
        expires_at: datetime,
    ) -> RefreshToken:

        refresh_token = RefreshToken(
            user_id=user_id,
            token_hash=token_hash,
            expires_at=expires_at,
        )

        self.session.add(refresh_token)
        await self.session.flush()

        return refresh_token

    async def get_by_hash(
        self,
        token_hash: str,
    ) -> RefreshToken | None:

        result = await self.session.execute(
            select(RefreshToken).where(RefreshToken.token_hash == token_hash),
        )

        return result.scalar_one_or_none()

    async def revoke_by_hash(self, token_hash: str) -> bool:
        refresh_token = await self.get_by_hash(token_hash)

        if refresh_token is None or refresh_token.revoked_at is not None:
            return False

        refresh_token.revoked_at = datetime.now(UTC)
        await self.session.flush()

        return True
