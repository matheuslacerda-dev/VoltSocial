from fastapi import Request, status
from fastapi.responses import JSONResponse

from app.exceptions.post import InvalidPostTitleError
from app.exceptions.user import UserAlreadyExistsError, UserNotFoundError


async def invalid_post_title_handler(
    request: Request,
    exc: InvalidPostTitleError,
) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
        content={
            "detail": str(exc),
        },
    )


async def user_not_found_handler(
    request: Request,
    exc: UserNotFoundError,
) -> JSONResponse:
    return JSONResponse(
        status_code=404,
        content={"detail": str(exc)},
    )


async def user_already_exists_handler(
    request: Request, exc: UserAlreadyExistsError
) -> JSONResponse:
    return JSONResponse(
        status_code=409,
        content={"detail": str(exc)},
    )
