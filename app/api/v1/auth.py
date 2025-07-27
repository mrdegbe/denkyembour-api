# ✅ << your login, register, token endpoints

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.core.security import verify_password, create_access_token  # your auth utils
from app.core.config import settings
from app.crud import user as crud_user
from app.models import user as models_user
from app.schemas import token as schemas_token  # optional, if you have a Token schema
from app.api.dependencies import get_db

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/login", response_model=schemas_token.Token)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    user = crud_user.get_user_by_email(db, form_data.username)
    verify_pass = verify_password(form_data.password, user.hashed_password)
    if not user:
        raise HTTPException(status_code=400, detail="Invalid email or password")
    if not verify_pass:
        raise HTTPException(status_code=400, detail="Invalid email or password")

    token_data = {
        "sub": str(user.id),
        "email": user.email,
        "role": str(user.role.value),
        "name": user.full_name,
    }

    exp_time = {settings.ACCESS_TOKEN_EXPIRE_MINUTES}

    access_token = create_access_token(data=token_data, expires_delta=exp_time)
    return {"access_token": access_token, "token_type": "bearer"}
