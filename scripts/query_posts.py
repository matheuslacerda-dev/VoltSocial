import asyncio

from sqlalchemy import select
from sqlalchemy.dialects import postgresql

from app.db.database import SessionLocal, engine
from app.models.post import Post


async def main():
    try:
        async with SessionLocal() as session:
            stmt = select(Post).order_by(Post.id.desc()).limit(5).offset(5)
            compiled = stmt.compile(
                dialect=postgresql.dialect(), compile_kwargs={"literal_binds": True}
            )

            print("SQL generated:")
            print(compiled)

            result = await session.execute(stmt)

            posts = result.scalars().all()

            print("posts founds:", {len(posts)})

            for post in posts:
                print(f"{post.id} | {post.title}")

    finally:
        await engine.dispose()


if __name__ == "__main__":
    asyncio.run(main())
