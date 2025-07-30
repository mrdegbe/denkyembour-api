from sqlalchemy.orm import Session
from app.models.news import News
from app.schemas.news import NewsCreate, NewsUpdate
from datetime import datetime
from typing import List, Optional

# Create a news post
def create_news(db: Session, news: NewsCreate) -> News:
    data = news.dict(exclude={"publish_date"})
    # db_news = News(**news.dict(), publish_date=news.publish_date or datetime.utcnow())
    db_news = News(**data, publish_date=news.publish_date or datetime.utcnow())
    db.add(db_news)
    db.commit()
    db.refresh(db_news)
    return db_news

# Get all news posts (optional filters: status, category)
def get_all_news(db: Session, skip: int = 0, limit: int = 10, status: Optional[str] = None, category: Optional[str] = None) -> List[News]:
    query = db.query(News)
    if status:
        query = query.filter(News.status == status)
    if category:
        query = query.filter(News.category == category)
    return query.offset(skip).limit(limit).all()

# Get single news post by ID
def get_news_by_id(db: Session, news_id: int) -> Optional[News]:
    return db.query(News).filter(News.id == news_id).first()

# Update news post
def update_news(db: Session, news_id: int, updates: NewsUpdate) -> Optional[News]:
    db_news = db.query(News).filter(News.id == news_id).first()
    if not db_news:
        return None
    for key, value in updates.dict(exclude_unset=True).items():
        setattr(db_news, key, value)
    db.commit()
    db.refresh(db_news)
    return db_news

# Delete news post
def delete_news(db: Session, news_id: int) -> bool:
    db_news = db.query(News).filter(News.id == news_id).first()
    if not db_news:
        return False
    db.delete(db_news)
    db.commit()
    return True

# Increment views count
def increment_views(db: Session, news_id: int) -> Optional[News]:
    db_news = db.query(News).filter(News.id == news_id).first()
    if not db_news:
        return None
    db_news.views += 1
    db.commit()
    db.refresh(db_news)
    return db_news
