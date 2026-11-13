from datetime import UTC, datetime

import pytest
from pydantic import ValidationError

from app.models.user import User
from app.schemas.user import UserCreate, UserRead


def test_valid_user_create():
    user = UserCreate(
        name="João Silva",
        username="joao_dev",
        email="joao@example.com",
        password="senha_segura_123",
    )
    assert user.username == "joao_dev"
    assert user.email == "joao@example.com"


def test_invalid_username():
    with pytest.raises(ValidationError):
        UserCreate(
            name="João Silva",
            username="joao dev",
            email="joao@example.com",
            password="senha_segura_123",
        )


def test_invalid_email():
    with pytest.raises(ValidationError):
        UserCreate(
            name="João Silva",
            username="joao_dev",
            email="email-invalido",
            password="senha_segura_123",
        )


def test_password_too_short():
    with pytest.raises(ValidationError):
        UserCreate(
            name="João Silva",
            username="joao_dev",
            email="joao@exemplo.com",
            password="avdcw",
        )


def test_normalize_user_identity():
    user = UserCreate(
        name="João Silva",
        username="  JOAO_DEV  ",
        email="JOAO@EXAMPLE.COM",
        password="senhasegura_123",
    )

    assert user.username == "joao_dev"
    assert user.email == "joao@example.com"


def test_user_read_does_not_expose_password_hash():
    now = datetime.now(UTC)

    user = User(
        id=1,
        name="joao silva",
        username="joao_silva",
        email="joao@example.com",
        password_hash="fake_hash_for_example",
        status="active",
        role="user",
        created_at=now,
        updated_at=now,
    )
    result = UserRead.model_validate(user)
    data = result.model_dump(mode="json")

    assert data["username"] == "joao_silva"
    assert "password_hash" not in data
    assert "password" not in data
