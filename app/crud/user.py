from datetime import datetime
from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.core.security import create_access_token, hash_password, verify_password
from app.models.user import User
import secrets, string

from app.schemas.user import UserCreate
from uuid import uuid4

# from app.schemas.user import UserUpdate


def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()


def login_user(db: Session, email: str, password: str):
    user = get_user_by_email(db, email)
    if not user or not verify_password(password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Invalid email or password")

    # Update last login
    user.last_login = datetime.utcnow()
    db.add(user)
    db.commit()
    db.refresh(user)

    # Token payload
    token_data = {
        "sub": str(user.id),
        "email": user.email,
        "role": str(user.role.value),
        "name": user.full_name,
    }
    access_token = create_access_token(data=token_data)
    return {"access_token": access_token, "token_type": "bearer"}


def create_user(db: Session, user_in: UserCreate):
    # Check if user already exists
    existing = db.query(User).filter(User.email == user_in.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    # 1. Generate random password
    password = "password"  # You can generate a random password here if needed
    # Example: password = ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(12))
    # Ensure the password meets your security requirements

    # 2. Hash it
    password_hash = hash_password(password)

    try:
        # 3. Create the user
        db_user = User(
            id=uuid4(),
            full_name=user_in.full_name,
            email=user_in.email,
            hashed_password=password_hash,  # Store the hashed password
            role=user_in.role,
            is_active=user_in.is_active,
            department=user_in.department,
            last_login=None,  # Set to None initially
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Failed to create user") from e


def list_users(db: Session, skip: int = 0, limit: int = 100):
    """
    Retrieve a list of users with optional pagination.
    """
    return db.query(User).offset(skip).limit(limit).all()


def update_user(db: Session, user_id, user_update):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Update only fields that are provided
    for field, value in user_update.dict(exclude_unset=True).items():
        setattr(user, field, value)

    db.commit()
    db.refresh(user)
    return user


def delete_user(db: Session, user_id):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(user)
    db.commit()
    return {"detail": "User deleted"}
