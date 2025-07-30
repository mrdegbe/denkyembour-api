import enum
from uuid import uuid4
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import (
    Column,
    Enum,
    Integer,
    String,
    Text,
    Boolean,
    ForeignKey,
    DateTime,
)
from sqlalchemy.orm import relationship
from app.core.database import Base
from datetime import datetime

from app.models.enums import NewsCategory, PostStatus


class News(Base):
    __tablename__ = "news"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    # excerpt = Column(Text, nullable=True)
    category = Column(
        Enum(
            NewsCategory,
            name="newscategoryenum",
            values_callable=lambda enum_cls: [e.value for e in enum_cls],
        ),
        nullable=False,
        index=True,
    )
    status = Column(
        Enum(
            PostStatus,
            name="poststatusenum",
            values_callable=lambda enum_cls: [e.value for e in enum_cls],
        ),
        default=PostStatus.draft,
        index=True,
    )
    content = Column(Text, nullable=False)
    # image_url = Column(String(512), nullable=True)  # Specify length
    # publish_date = Column(Boolean, default=False, index=True)  # Add index
    author_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True, default=uuid4)
    publish_date = Column(DateTime, default=datetime.utcnow, index=True)
    views = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


    author = relationship("User", back_populates="news_posts")

    def __repr__(self):
        return f"<News(id={self.id}, title={self.title}, published={self.published})>"


# In your User model, add:
# news = relationship("News", back_populates="author")
