import asyncio

from sqlalchemy import inspect

from app.db.database import SessionLocal, engine
from app.models.post import Post


async def main():
    try:
        post = Post(
            title="Testing ORM States",
            content="testing orm states",
        )
        print("Transient:", inspect(post).transient)
        async with SessionLocal() as session:
            session.add(post)

            print("Pending:", inspect(post).pending)

            await session.flush()

            print("Persinstent:", inspect(post).persistent)
            print("Generated ID:", post.id)

            await session.rollback()

            print("Transient after rollback:", inspect(post).transient)
    finally:
        await engine.dispose()


if __name__ == "__main__":
    asyncio.run(main())
