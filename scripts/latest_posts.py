import asyncio

from sqlalchemy import select

from app.db.database import SessionLocal, engine
from app.models.post import Post


async def main():
    try:
        async with SessionLocal() as session:
            stmt = select(Post).order_by(Post.id.desc()).limit(3)
            result = await session.execute(stmt)
            posts = result.scalars().all()

            if not posts:
                print("does not exists any post there")
            else:
                print("the 3 posts with the biggest ID:")
                for post in posts:
                    print(f"{post.id} | {post.title} | {post.created_at}")

    finally:
        await engine.dispose()


if __name__ == "__main__":
    asyncio.run(main())
