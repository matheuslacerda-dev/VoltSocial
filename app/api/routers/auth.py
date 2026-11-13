from fastapi import APIRouter, status

from app.api.dependencies import AuthServiceDep
from app.schemas.user import UserCreate, UserRead

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


@router.post(
    "/register",
    response_model=UserRead,
    status_code=status.HTTP_201_CREATED,
)
async def register(
    data: UserCreate,
    auth_service: AuthServiceDep,
) -> UserRead:
    return await auth_service.register(data)
