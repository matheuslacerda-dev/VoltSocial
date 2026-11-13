from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.core.config import get_settings
from app.db.database import engine

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    print(f"{settings.app_name}: Starting Application...")
    try:
        yield
    finally:
        await engine.dispose()
        print(f"{settings.app_name}: Stopping Application...")
