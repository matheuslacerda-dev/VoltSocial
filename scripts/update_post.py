import asyncio

from sqlalchemy import inspect, select

from app.db.database import SessionLocal, engine
from app.models.post import Post


async def main():
    try:
        async with SessionLocal() as session:
            result = await session.execute(select(Post).order_by(Post.id).limit(1))
            post = result.scalar_one_or_none()

            if post is None:
                print("no one post found")
                return

            print("Original title:", post.title)

            post.title = "updated by ORM"

            print("Modified Object?", post in session.dirty)
            print(
                "Updated title?",
                inspect(post).attrs.title.history.has_changes(),
            )
            await session.flush()

            print("UPDATE sent to DB")
            await session.commit()
            print("transaction done!")

    finally:
        await engine.dispose()


if __name__ == "__main__":
    asyncio.run(main())
