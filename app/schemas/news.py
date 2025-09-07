from datetime import datetime
from typing import Optional
from pydantic import BaseModel
from app.models.enums import NewsCategory, PostStatus

# from sqlalchemy.dialects.postgresql import UUID
from uuid import UUID


class NewsBase(BaseModel):
    title: str
    category: NewsCategory
    status: PostStatus = PostStatus.draft
    publish_date: Optional[datetime] = None
    views: Optional[int] = 0


class NewsCreate(NewsBase):
    author_id: UUID
    content: str  # Assuming content is required for creation

    model_config = {"arbitrary_types_allowed": True}  # ✅ v2-compliant


class NewsUpdate(BaseModel):
    title: Optional[str]
    category: Optional[NewsCategory]
    status: Optional[PostStatus]
    publish_date: Optional[datetime]


class AuthorOut(BaseModel):
    id: int
    full_name: str

    class Config:
        orm_mode = True


class NewsOut(NewsBase):
    id: int
    author: AuthorOut

    class Config:
        orm_mode = True
