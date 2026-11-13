import asyncio

from sqlalchemy import text

from app.db.database import engine


async def main():
    try:
        async with engine.connect() as connection:
            result = await connection.execute(text("SELECT 1"))
            print("Result:", result.scalar_one())
            print("Connection with PostgreSQL done!")

    finally:
        await engine.dispose()


if __name__ == "__main__":
    asyncio.run(main())
