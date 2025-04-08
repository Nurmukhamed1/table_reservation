from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from src.configs import Base


class Table(Base):
    __tablename__ = "table"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    seats = Column(Integer, nullable=False)
    location = Column(String, nullable=False)

    reservations = relationship("Reservation", back_populates="table")
