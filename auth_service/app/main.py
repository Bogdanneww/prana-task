from fastapi import FastAPI
from app.routers.auth import router as auth_router
from app.routers.health import router as health_router

app = FastAPI(title="Auth Service", version="1.0.0")

app.include_router(health_router, tags=["health"])
app.include_router(auth_router, prefix="/auth", tags=["auth"])
