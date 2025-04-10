from fastapi import APIRouter

from api.v1.routers import v1_router

main_router = APIRouter()

main_router.include_router(v1_router)
