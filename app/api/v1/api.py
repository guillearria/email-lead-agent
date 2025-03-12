from fastapi import APIRouter

from app.api.v1.endpoints import auth, gmail

api_router = APIRouter()

# Include routers
api_router.include_router(auth.router, prefix="/auth", tags=["authentication"])
api_router.include_router(gmail.router, prefix="/gmail", tags=["gmail"]) 