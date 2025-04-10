from typing import Optional, List
from fastapi import Query
from sqlalchemy import Select
from models.reservation import Reservation


class ReservationFilter:
    def __init__(
            self,
            ids: Optional[List[int]] = Query(None),
            table_id: Optional[int] = Query(None)
    ):
        self.ids = ids
        self.table_id = table_id

    def apply_filters(self, query: Select) -> Select:
        if self.ids:
            query = query.where(Reservation.id.in_(self.ids))
        if self.table_id:
            query = query.where(Reservation.table_id == self.table_id)
        return query
