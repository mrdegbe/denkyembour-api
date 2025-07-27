from sqlalchemy import (
    Column,
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


class News(Base):
    __tablename__ = "news"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    excerpt = Column(Text, nullable=True)
    content = Column(Text, nullable=False)
    image_url = Column(String(512), nullable=True)  # Specify length
    published = Column(Boolean, default=False, index=True)  # Add index
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    author_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    author = relationship("User", back_populates="news")

    def __repr__(self):
        return f"<News(id={self.id}, title={self.title}, published={self.published})>"


# In your User model, add:
# news = relationship("News", back_populates="author")
