import traceback
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.api.dependencies import get_db
from app.models.user import User
from app.schemas.user import UserCreate, UserOut  # You need to define these schemas
from uuid import uuid4
from app.crud.user import (
    create_user as crud_user,
    list_users as crud_list_users,
    update_user as crud_update_user,
    delete_user as crud_delete_user,
)

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def create_user(user_in: UserCreate, db: Session = Depends(get_db)):
    try:
        return crud_user(db, user_in)
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/", response_model=list[UserOut])
def get_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    try:
        return crud_list_users(db, skip=skip, limit=limit)
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/{user_id}/", response_model=UserOut)
def update_user_endpoint(
    user_id: str, user_update: UserCreate, db: Session = Depends(get_db)
):
    try:
        return crud_update_user(db, user_id, user_update)
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{user_id}/", status_code=status.HTTP_200_OK)
def delete_user_endpoint(user_id: str, db: Session = Depends(get_db)):
    try:
        return crud_delete_user(db, user_id)
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))
