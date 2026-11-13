import asyncio

from sqlalchemy.exc import IntegrityError

from app.db.database import SessionLocal, engine
from app.models.user import User


def make_user(username: str, email: str) -> User:
    return User(
        name="usuario de teste",
        username=username,
        email=email,
        password_hash="TEST_ONLY_NOT_A_REAL_HASH",
    )


async def main():
    try:
        async with SessionLocal() as session:
            try:
                first_user = make_user(
                    username="Joao_dev",
                    email="joao1@example.com",
                )
                session.add(first_user)
                await session.flush()

                print("Primeiro usuario inserido na transação.")

                second_user = make_user(
                    username="JOAO_DEV",
                    email="joao2@example.com",
                )
                session.add(second_user)

                try:
                    await session.flush()
                except IntegrityError:
                    print("SUCESSO: postgresql rejeitou o username duplicado!")
                else:
                    raise AssertionError(
                        "ERRO: o banco de dados aceitou usernames equivalentes!"
                    )

            finally:
                await session.rollback()
                print("Transação revertida. Nenhum usuário de teste foi salvo.")
    finally:
        await engine.dispose()


if __name__ == "__main__":
    asyncio.run(main())
