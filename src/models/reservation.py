from fastapi import HTTPException
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.util.preloaded import orm

from src.configs import Base


class Reservation(Base):
    __tablename__ = "reservation"

    id = Column(Integer, primary_key=True, autoincrement=True)
    reservation_time = Column(DateTime, nullable=False)
    duration_minutes = Column(Integer, nullable=False)

    table_id = Column(Integer, ForeignKey("table.id"), nullable=True)
    table = relationship("Table", back_populates="reservations")

    @orm.validates("duration_minutes")
    def validate_duration_minutes(self, key, duration_minutes):
        if duration_minutes <= 0:
            raise HTTPException(status_code=400, detail="Duration must be greater than 0 minutes")
        return duration_minutes
