from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from app.schemas.news import NewsCreate, NewsOut, NewsUpdate
from app.crud import news as crud
from app.api.dependencies import get_db

router = APIRouter(prefix="/news", tags=["News"])


# ✅ Create news
@router.post("/", response_model=NewsCreate, status_code=status.HTTP_201_CREATED)
def create_news(news: NewsCreate, db: Session = Depends(get_db)):
    return crud.create_news(db, news)


# ✅ List all news (with optional filters)
@router.get("/", response_model=List[NewsOut])
def list_news(
    skip: int = 0,
    limit: int = 10,
    status: Optional[str] = None,
    category: Optional[str] = None,
    db: Session = Depends(get_db),
):
    return crud.get_all_news(
        db, skip=skip, limit=limit, status=status, category=category
    )


# ✅ Get news by ID
@router.get("/{news_id}", response_model=NewsOut)
def get_news(news_id: int, db: Session = Depends(get_db)):
    db_news = crud.get_news_by_id(db, news_id)
    if not db_news:
        raise HTTPException(status_code=404, detail="News not found")
    return db_news


# ✅ Update news
@router.put("/{news_id}", response_model=NewsOut)
def update_news(news_id: int, news_update: NewsUpdate, db: Session = Depends(get_db)):
    updated = crud.update_news(db, news_id, news_update)
    if not updated:
        raise HTTPException(status_code=404, detail="News not found")
    return updated


# ✅ Delete news
@router.delete("/{news_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_news(news_id: int, db: Session = Depends(get_db)):
    deleted = crud.delete_news(db, news_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="News not found")
    return


# ✅ Increment views (e.g., when news is viewed publicly)
@router.post("/{news_id}/view", response_model=NewsCreate)
def increment_news_views(news_id: int, db: Session = Depends(get_db)):
    updated = crud.increment_views(db, news_id)
    if not updated:
        raise HTTPException(status_code=404, detail="News not found")
    return updated
