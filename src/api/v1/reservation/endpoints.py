from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_utils.cbv import cbv
from sqlalchemy import select
from sqlalchemy.orm import Session

from configs import get_db
from core.pagination import Page, paginate, PaginationParams
from models.reservation import Reservation
from .filters import ReservationFilter
from .schema import ReservationSchema, ReservationCreate

reservation_router = APIRouter()


@cbv(reservation_router)
class ReservationView:
    database: Session = Depends(get_db)

    @reservation_router.get("/", response_model=Page[ReservationSchema])
    def list(self, filters: ReservationFilter = Depends(), pagination: PaginationParams = Depends()):
        query = select(Reservation)
        query = filters.apply_filters(query)
        return paginate(self.database, query, pagination)

    @reservation_router.post("/", response_model=ReservationSchema)
    def create(self, data: ReservationCreate):
        end_time = data.reservation_time + timedelta(minutes=data.duration_minutes)

        overlapping = self.db.execute(
            select(Reservation).where(
                Reservation.table_id == data.table_id,
                Reservation.reservation_time < end_time,
                (Reservation.reservation_time + timedelta(minutes=Reservation.duration_minutes)) > data.reservation_time
            )
        ).scalars().first()

        if overlapping:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Table is already reserved during this time slot"
            )

        new_reservation = Reservation(**data.dict())
        self.db.add(new_reservation)
        self.db.commit()
        self.db.refresh(new_reservation)
        return new_reservation_
