import asyncio

from sqlalchemy import select

from app.db.database import SessionLocal, engine
from app.models.post import Post


async def main():
    try:
        async with SessionLocal() as session:
            post = Post(
                title="second post, test rollback",
                content="wont exist",
            )
            session.add(post)

            await session.flush()
            post_id = post.id

            print("id generated", post_id)
            await session.rollback()
            print("rollback executed")

        async with SessionLocal() as session:
            stmt = select(Post).where(Post.id == post_id)

            result = await session.execute(stmt)
            saved_post = result.scalar_one_or_none()
            print("post founded", saved_post)
    finally:
        await engine.dispose()


if __name__ == "__main__":
    asyncio.run(main())
