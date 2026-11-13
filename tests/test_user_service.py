from unittest.mock import AsyncMock

import pytest

from app.exceptions.user import UserNotFoundError
from app.repositories.user import UserRepository
from app.services.user import UserService


@pytest.mark.anyio
async def test_get_user_not_found():
    repository = AsyncMock(spec=UserRepository)
    repository.get_by_id.return_value = None

    service = UserService(repository)

    with pytest.raises(UserNotFoundError):
        await service.get_user(99999999)

    repository.get_by_id.assert_awaited_once_with(99999999)
