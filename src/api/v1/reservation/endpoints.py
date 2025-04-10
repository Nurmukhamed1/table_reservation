from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException
from fastapi_utils.cbv import cbv
from sqlalchemy import select
from sqlalchemy.orm import Session

from configs import get_db
from core.logger import logger
from core.pagination import Page, paginate, PaginationParams
from models import Table
from models.reservation import Reservation
from .filters import ReservationFilter
from .schema import ReservationReadSchema, ReservationSchema

reservation_router = APIRouter()


@cbv(reservation_router)
class ReservationView:
    database: Session = Depends(get_db)

    @reservation_router.get("/", response_model=Page[ReservationReadSchema])
    def list(self, filters: ReservationFilter = Depends(), pagination: PaginationParams = Depends()):
        query = select(Reservation)
        query = filters.apply_filters(query)
        return paginate(self.database, query, pagination)

    @reservation_router.post("/", response_model=ReservationSchema)
    def create(self, data: ReservationSchema):
        self.check_table(data.table_id)
        self.check_reservation_time(data)

        reservation = Reservation(**data.model_dump())
        self.database.add(reservation)
        self.database.commit()
        self.database.refresh(reservation)
        logger.info(f"Reservation created: id={reservation.id}, table_id={reservation.table_id}")
        return reservation

    @reservation_router.delete("/{reservation_id}", response_model=ReservationSchema)
    def delete(self, reservation_id: int):
        reservation = self.database.get(Reservation, reservation_id)
        if not reservation:
            raise HTTPException(status_code=404, detail="Reservation not found")

        self.database.delete(reservation)
        self.database.commit()
        logger.info(f"Reservation {reservation_id} deleted")
        return reservation

    def check_table(self, table_id: int) -> None:
        table = self.database.get(Table, table_id)
        if not table:
            logger.warning(f"Attempt to create reservation for non-existent table_id={table_id}")
            raise HTTPException(status_code=404, detail="Table not found")

    def check_reservation_time(self, data: ReservationSchema) -> None:
        start_time = data.reservation_time
        end_time = start_time + timedelta(minutes=data.duration_minutes)

        stmt = select(Reservation).where(
            Reservation.table_id == data.table_id,
            Reservation.reservation_time < end_time,
            (Reservation.reservation_time + timedelta(minutes=data.duration_minutes)) > start_time
        )

        reserved = self.database.execute(stmt).scalars().first()
        if reserved:
            logger.info(f"Conflict reservation: table_id={data.table_id} reservation_time={reserved.reservation_time}")
            raise HTTPException(status_code=409, detail="The table is already reserved")
