from fastapi import APIRouter, Depends, HTTPException
from fastapi_utils.cbv import cbv
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from models import Table
from .filters import TableFilter
from configs import get_db
from core.pagination import Page, paginate, PaginationParams
from .schema import TableReadSchema, TableSchema

table_router = APIRouter()


@cbv(table_router)
class TableView:
    database: Session = Depends(get_db)

    @table_router.get("/", response_model=Page[TableReadSchema])
    def list(self, filters: TableFilter = Depends(), pagination: PaginationParams = Depends()):
        query = select(Table)
        query = filters.apply_filters(query)
        return paginate(self.database, query, pagination)

    @table_router.post("/", response_model=TableSchema)
    def create(self, data: TableSchema):
        new_table = Table(**data.model_dump())
        self.database.add(new_table)
        try:
            self.database.commit()
            self.database.refresh(new_table)
        except IntegrityError as e:
            self.database.rollback()
            raise HTTPException(status_code=400, detail=f"Table with {new_table.id} id already exists")
        return new_table

    @table_router.put("/{table_id}", response_model=TableSchema)
    def update(self, table_id: int, data: TableSchema):
        table = self.database.get(Table, table_id)
        if not table:
            raise HTTPException(status_code=404, detail="Table not found")

        for key, value in data.model_dump().items():
            setattr(table, key, value)

        self.database.commit()
        self.database.refresh(table)
        return table

    @table_router.delete("/{table_id}", response_model=TableSchema)
    def delete(self, table_id: int):
        table = self.database.get(Table, table_id)
        if not table:
            raise HTTPException(status_code=404, detail="Table not found")

        self.database.delete(table)
        self.database.commit()
        return table