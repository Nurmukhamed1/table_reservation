from fastapi import APIRouter

from api.v1.table.endpoints import table_router
from api.v1.reservation.endpoints import reservation_router

main_router = APIRouter()

main_router.include_router(table_router, prefix="/table", tags=["table"])
main_router.include_router(reservation_router, prefix="/reservation", tags=["reservation"])
