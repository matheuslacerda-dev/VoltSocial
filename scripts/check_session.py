import asyncio

from sqlalchemy import text

from app.db.database import SessionLocal, engine


async def main():
    try:
        async with SessionLocal() as session:
            result = await session.execute(text("SELECT 1"))
            value = result.scalar_one()

            print(f"Result: {value}")
            print(f"Session open: {session.is_active}")

        print("Session closed with success!")

    finally:
        await engine.dispose()


if __name__ == "__main__":
    asyncio.run(main())
