from fastapi import HTTPException
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.util.preloaded import orm

from src.configs import Base


class Table(Base):
    __tablename__ = "table"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    seats = Column(Integer, nullable=False)
    location = Column(String, nullable=False)

    reservations = relationship("Reservation", back_populates="table")

    @orm.validates("seats")
    def validate_seats(self, key, seats):
        if seats <= 0:
            raise HTTPException(status_code=400, detail="Seats must be greater than 0")
        return seats
