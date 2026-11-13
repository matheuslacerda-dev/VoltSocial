from fastapi import FastAPI

from app.api.router import api_router
from app.core.config import get_settings
from app.core.lifespan import lifespan
from app.exceptions.handlers import (
    invalid_post_title_handler,
    user_already_exists_handler,
    user_not_found_handler,
)
from app.exceptions.post import InvalidPostTitleError
from app.exceptions.user import UserAlreadyExistsError, UserNotFoundError

settings = get_settings()
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    debug=settings.debug,
    lifespan=lifespan,
)

app.add_exception_handler(
    InvalidPostTitleError,
    invalid_post_title_handler,
)
app.add_exception_handler(
    UserNotFoundError,
    user_not_found_handler,
)
app.add_exception_handler(
    UserAlreadyExistsError,
    user_already_exists_handler,
)
app.include_router(api_router)


@app.get("/")
async def home():
    return {"message": "welcome to VoltSocial"}
