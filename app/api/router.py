from fastapi import APIRouter

from app.api.routers import health, posts, users
from app.api.routers.auth import router as auth_router

api_router = APIRouter()

api_router.include_router(health.router)
api_router.include_router(posts.router)
api_router.include_router(users.router)
api_router.include_router(auth_router)
