from uuid import uuid4
from datetime import datetime
from sqlalchemy import Column, String, Boolean, DateTime, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.core.database import Base
from app.models.enums import RoleEnum


class User(Base):
    __tablename__ = "users"

    id = Column(UUID, primary_key=True, index=True, default=uuid4)
    full_name = Column(String)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    role = Column(
        Enum(
            RoleEnum,
            name="usersroleenum",
            values_callable=lambda enum_cls: [e.value for e in enum_cls],
        )
    )
    department = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    last_login = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)


    # Relationship with News
    # Assuming a user can author multiple news posts
    news_posts = relationship("News", back_populates="author")

    def __repr__(self):
        return f"<User(id={self.id}, email={self.email}, role={self.role})>"
