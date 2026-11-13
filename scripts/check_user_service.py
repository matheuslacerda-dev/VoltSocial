import asyncio

from app.db.database import SessionLocal, engine
from app.exceptions.user import UserNotFoundError
from app.repositories.user import UserRepository
from app.services.user import UserService


async def main():
    try:
        async with SessionLocal() as session:
            repository = UserRepository(session)
            service = UserService(repository)

            users = await service.list_users(limit=10)

            print("Users:", users)
            print("Total:", len(users))

            try:
                user = await service.get_user(99999)
                print("User not found", user.username)
            except UserNotFoundError as exc:
                print("Business error:", exc)

    finally:
        await engine.dispose()


if __name__ == "__main__":
    asyncio.run(main())
