import asyncio

from sqlalchemy import select

from app.db.database import SessionLocal, engine
from app.models.post import Post


async def main():
    try:
        async with SessionLocal() as session:
            stmt = select(Post).order_by(Post.id).limit(1)
            result = await session.execute(stmt)
            post_a = result.scalar_one_or_none()

            print("Post A:", post_a.id, post_a.title)
        async with SessionLocal() as session:
            stmt = select(Post).order_by(Post.id).limit(1)
            result = await session.execute(stmt)
            post_b = result.scalar_one_or_none()
            print("Post B:", post_b.id, post_b.title)

        print("it is the same?", post_a is post_b)

    finally:
        await engine.dispose()


if __name__ == "__main__":
    asyncio.run(main())
