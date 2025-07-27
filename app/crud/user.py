from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.core.security import hash_password
from app.models.user import User
import secrets, string

from app.schemas.user import UserCreate
from uuid import uuid4

# from app.schemas.user import UserUpdate


def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()


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
            is_active=True,
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


# def update_user(db: Session, user_id: int, user_update: UserUpdate):
#     user = db.query(User).filter(User.id == user_id).first()
#     if not user:
#         raise HTTPException(status_code=404, detail="User not found")

#     # Update only fields that were sent
#     if user_update.name is not None:
#         user.name = user_update.name

#     db.commit()
#     db.refresh(user)
#     return user
