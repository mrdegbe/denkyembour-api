import os
from uuid import uuid4
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from getpass import getpass

# Import your models and hash_password function
from app.core.database import Base
from app.core.security import hash_password
from app.models import User  # adjust path as needed
# from app.security import hash_password  # adjust path as needed

# 1. Get database URL from environment or hardcode for testing
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@localhost:5432/dbname")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def create_admin():
    db = SessionLocal()
    try:
        email = "mrdegbe@dda.gov.gh"
        full_name = "Raymond Degbe"
        password = "password"  # For security, consider using getpass("Enter password for admin: ")

        # Check if admin already exists
        existing = db.query(User).filter(User.email == email).first()
        if existing:
            print(f"❌ User with email {email} already exists.")
            return

        admin_user = User(
            id=uuid4(),
            full_name=full_name,
            email=email,
            hashed_password=hash_password(password),
            role="admin",
            is_active=True,
            department="Administration",
            last_login=None,
        )

        db.add(admin_user)
        db.commit()
        print("✅ Admin user created successfully!")

    except Exception as e:
        db.rollback()
        print("❌ Failed to create admin:", e)
    finally:
        db.close()

if __name__ == "__main__":
    # Ensure tables exist (optional, if Alembic hasn’t run yet)
    Base.metadata.create_all(bind=engine)
    create_admin()
