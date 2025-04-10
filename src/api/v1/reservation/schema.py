from pydantic import BaseModel
from datetime import datetime


class ReservationReadSchema(BaseModel):
    id: int
    table_id: int
    reservation_time: datetime
    duration_minutes: int

    class Config:
        orm_mode = True


class ReservationSchema(BaseModel):
    table_id: int
    reservation_time: datetime
    duration_minutes: int
