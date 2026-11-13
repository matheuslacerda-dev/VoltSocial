from app.exceptions.post import InvalidPostTitleError
from app.schemas.post import PostCreate


class PostService:
    def create_post(self, data: PostCreate) -> dict:
        if not data.title.strip():
            raise InvalidPostTitleError("The title can't have only spaces.")
        return {
            "id": 1,
            "title": data.title,
            "content": data.content,
        }
