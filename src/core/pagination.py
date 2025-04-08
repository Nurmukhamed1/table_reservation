from typing import TypeVar, Generic, List

from fastapi import Query
from pydantic import BaseModel
from pydantic.generics import GenericModel
from sqlalchemy import Select, func
from sqlalchemy import select
from sqlalchemy.orm import Session

T = TypeVar("T")


class PageMeta(BaseModel):
    total: int
    page: int
    size: int


class Page(GenericModel, Generic[T]):
    items: List[T]
    meta: PageMeta


class PaginationParams(BaseModel):
    page: int = Query(1, ge=1)
    size: int = Query(10, ge=1, le=100)


def paginate(
        db: Session,
        query: Select,
        params: PaginationParams
):
    total = db.scalar(select(func.count()).select_from(query.subquery()))
    results = db.execute(query.offset((params.page - 1) * params.size).limit(params.size))
    items = results.scalars().all()

    return Page(
        items=items,
        meta=PageMeta(total=total, page=params.page, size=params.size)
    )
