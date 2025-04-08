from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from src.configs import Base


class Reservation(Base):
    __tablename__ = "reservation"

    id = Column(Integer, primary_key=True, autoincrement=True)
    customer_name = Column(String, nullable=False)
    reservation_time = Column(DateTime, nullable=False)
    duration_minutes = Column(Integer, nullable=False)

    table_id = Column(Integer, ForeignKey("table.id"), nullable=True)
    table = relationship("Table", back_populates="reservations")
