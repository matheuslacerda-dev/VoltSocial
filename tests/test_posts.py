from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_create_post_success():
    response = client.post(
        "/posts/",
        json={
            "title": "my first test",
            "content": "testing my fastapi app",
        },
    )
    assert response.status_code == 201

    data = response.json()


def test_create_post_with_blank_title():
    response = client.post(
        "/posts/",
        json={
            "title": "    ",
            "content": "testing blank title",
        },
    )
    assert response.status_code == 422
    assert response.json() == {"detail": "The title can't have only spaces."}


def test_with_short_title():
    response = client.post(
        "/posts/",
        json={
            "title": "hi",
            "content": "testing with short title",
        },
    )
    assert response.status_code == 422
    errors = response.json()["detail"]

    assert any(error["loc"] == ["body", "title"] for error in errors)
