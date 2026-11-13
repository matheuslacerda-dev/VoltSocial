import asyncio

from app.db.database import SessionLocal, engine
from app.repositories.user import UserRepository


async def main():
    try:
        async with SessionLocal() as session:
            repository = UserRepository(session)

            user_by_id = await repository.get_by_id(9999999)
            user_by_username = await repository.get_by_username("usuario_inexistente")
            user_by_email = await repository.get_by_email("inexistente@gmail.com")

            print("By id:", user_by_id)
            print("By username:", user_by_username)
            print("By email:", user_by_email)

            users = await repository.list_users(limit=5)
            print("total users:", len(users))
            print("users:", users)
            assert isinstance(users, list)
            assert len(users) <= 5
    finally:
        await engine.dispose()


if __name__ == "__main__":
    asyncio.run(main())
