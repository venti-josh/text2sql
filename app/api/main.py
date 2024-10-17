from fastapi import APIRouter

from app.api.routes import sql

api_router = APIRouter()
api_router.include_router(sql.router, prefix="/sql", tags=["queries"])
