from pydantic import BaseModel, Field


class PostCreate(BaseModel):
    title: str = Field(min_length=3, max_length=120)
    content: str = Field(min_length=4)


class PostRead(BaseModel):
    id: int
    title: str
    content: str
