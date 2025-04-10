from pydantic import BaseModel


class TableReadSchema(BaseModel):
    id: int
    name: str
    seats: int
    location: str

    class Config:
        orm_mode = True


class TableSchema(BaseModel):
    name: str
    seats: int
    location: str
