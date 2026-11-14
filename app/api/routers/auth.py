from fastapi import APIRouter, status

from app.api.dependencies import AuthServiceDep, CurrentUserDep
from app.schemas.auth import LoginRequest, RefreshRequest, TokenResponse
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


@router.post(
    "/login",
    response_model=TokenResponse,
)
async def login(
    data: LoginRequest,
    auth_service: AuthServiceDep,
) -> TokenResponse:
    tokens = await auth_service.login(
        email=str(data.email),
        password=data.password,
    )
    return TokenResponse(
        access_token=tokens.access_token,
        refresh_token=tokens.refresh_token,
    )


@router.get("/me", response_model=UserRead)
async def get_me(
    current_user: CurrentUserDep,
) -> UserRead:
    return UserRead.model_validate(current_user)


@router.post("/refresh", response_model=TokenResponse)
async def refresh(
    data: RefreshRequest,
    auth_service: AuthServiceDep,
) -> TokenResponse:
    tokens = await auth_service.refresh(data.refresh_token)

    return TokenResponse(
        access_token=tokens.access_token,
        refresh_token=tokens.refresh_token,
    )


@router.post(
    "/logout",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def logout(
    data: RefreshRequest,
    auth_service: AuthServiceDep,
) -> None:
    await auth_service.logout(data.refresh_token)
