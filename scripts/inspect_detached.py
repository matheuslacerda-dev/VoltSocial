import asyncio

from sqlalchemy import inspect, select

from app.db.database import SessionLocal, engine
from app.models.post import Post


async def main():
    try:
        async with SessionLocal() as session:
            result = await session.execute(select(Post).limit(1))
            post = result.scalar_one_or_none()

            if post is None:
                print("No one post found")
                return

            print("inside session:", inspect(post).persistent)
        print("outside session:", inspect(post).detached)
        print("loaded title:", post.title)
    finally:
        await engine.dispose()


if __name__ == "__main__":
    asyncio.run(main())
