from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.database import Base, engine  # ✅ Use your new core.database
from app.api.v1 import auth, news, user as user_router  # ✅ Import your routers

# ✅ Create all tables — in prod you'd do this with Alembic, not at runtime
Base.metadata.create_all(bind=engine)

# ✅ Instantiate FastAPI app
app = FastAPI(
    title="Denkyembour CMS",
    version="1.0.0",
)

# ✅ CORS Middleware (put real origins in prod)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:8080",
    ],  # Replace with allowed origins in production!
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Include routers
app.include_router(auth.router)
app.include_router(user_router.router)
app.include_router(news.router) 
