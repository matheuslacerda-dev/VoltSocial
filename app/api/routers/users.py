from fastapi import APIRouter, Query

from app.api.dependencies import UserServiceDep
from app.schemas.user import UserRead

router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


@router.get("/", response_model=list[UserRead])
async def list_user(
    user_service: UserServiceDep,
    limit: int = Query(default=10, ge=1, le=100),
):
    return await user_service.list_users(limit=limit)


@router.get("/{user_id}", response_model=UserRead)
async def get_user(
    user_id: int,
    user_service: UserServiceDep,
):
    return await user_service.get_user(user_id)
