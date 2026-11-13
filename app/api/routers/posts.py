from fastapi import APIRouter, status

from app.api.dependencies import PostServiceDep
from app.schemas.post import PostCreate, PostRead

router = APIRouter(
    prefix="/posts",
    tags=["Posts"],
)


@router.get("/")
async def list_posts():
    return {"items": []}


@router.get("/{post_id}", response_model=PostRead)
async def get_post(post_id: int):
    return {
        "id": post_id,
        "title": "Exemplo",
        "content": "conteudo temporario",
    }


@router.post(
    "/",
    response_model=PostRead,
    status_code=status.HTTP_201_CREATED,
)
def create_post(
    data: PostCreate,
    post_service: PostServiceDep,
):
    return post_service.create_post(data)
