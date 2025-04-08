from typing import Optional, List

from fastapi import Query
from sqlalchemy import Select

from models import Table


class TableFilter:
    def __init__(
            self,
            ids: Optional[List[int]] = Query(None),
            name: Optional[List[str]] = Query(None),
            seats: Optional[List[int]] = Query(None),
            location: Optional[List[str]] = Query(None),
            search: Optional[str] = Query(None),
    ):
        self.ids = ids
        self.name = name
        self.seats = seats
        self.location = location
        self.search = search

    def apply_filters(self, query: Select) -> Select:
        if self.ids:
            query = query.where(Table.id.in_(self.ids))
        if self.name:
            query = query.where(Table.name.in_(self.name))
        if self.seats:
            query = query.where(Table.seats.in_(self.seats))
        if self.location:
            query = query.where(Table.location.in_(self.location))
        if self.search:
            query = query.where(
                Table.name.ilike(f"%{self.search}%") |
                Table.location.ilike(f"%{self.search}%")
            )
        return query
