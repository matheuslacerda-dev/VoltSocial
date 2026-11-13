import asyncio

from sqlalchemy import select

from app.db.database import SessionLocal, engine
from app.models.post import Post


async def main():
    try:
        async with SessionLocal() as session:
            post = Post(
                title="for the ai gain",
                content="you must have the ai pain",
            )

            session.add(post)

            print("before flush", post.id)

            await session.flush()

            print("after flush", post.id)

            await session.commit()

            await session.refresh(post)

            print("post saved", post.id, post.title)

            print("post created in", post.created_at)

        async with SessionLocal() as session:
            stmt = select(Post).where(Post.id == post.id)
            result = await session.execute(stmt)
            saved_post = result.scalar_one_or_none()

            print("post recovered", saved_post)

    finally:
        await engine.dispose()


if __name__ == "__main__":
    asyncio.run(main())
