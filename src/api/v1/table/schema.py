from pydantic import BaseModel


class TableSchema(BaseModel):
    id: int
    name: str
    seats: int
    location: str

    class Config:
        orm_mode = True
