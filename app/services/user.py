from app.exceptions.user import UserAlreadyExistsError, UserNotFoundError
from app.models.user import User
from app.repositories.user import UserRepository


class UserService:
    def __init__(self, repository: UserRepository) -> None:
        self.repository = repository

    async def get_user(self, user_id: int) -> User:
        user = await self.repository.get_by_id(user_id)

        if user is None:
            raise UserNotFoundError(user_id)

        return user

    async def list_users(self, limit: int = 10) -> list[User]:
        return await self.repository.list_users(limit=limit)

    async def ensure_identity_available(
        self,
        username: str,
        email: str,
    ) -> None:
        existing_username = await self.repository.get_by_username(
            username,
        )
        if existing_username is not None:
            raise UserAlreadyExistsError("username")

        existing_email = await self.repository.get_by_email(
            email,
        )
        if existing_email is not None:
            raise UserAlreadyExistsError("email")
