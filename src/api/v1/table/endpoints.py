from fastapi import APIRouter, Depends
from fastapi_utils.cbv import cbv
from sqlalchemy import select
from sqlalchemy.orm import Session

from models import Table
from .filters import TableFilter
from configs import get_db
from core.pagination import Page, paginate, PaginationParams
from .schema import TableSchema

table_router = APIRouter()


@cbv(table_router)
class TableView:
    database: Session = Depends(get_db)

    @table_router.get("/", response_model=Page[TableSchema])
    def list(self, filters: TableFilter = Depends(), pagination: PaginationParams = Depends()):
        query = select(Table)
        query = filters.apply_filters(query)
        return paginate(self.database, query, pagination)
