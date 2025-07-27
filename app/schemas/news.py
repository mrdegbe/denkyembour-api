from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class NewsPostBase(BaseModel):
    title: str
    excerpt: Optional[str] = None
    content: str
    image_url: Optional[str] = None
    published: bool


class NewsPostCreate(NewsPostBase):
    pass


class NewsPostUpdate(NewsPostBase):
    pass


class NewsPostOut(NewsPostBase):
    id: int
    created_at: datetime
    updated_at: datetime
    author_id: Optional[int]

    class Config:
        orm_mode = True
