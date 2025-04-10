from pydantic import BaseModel


class TableReadSchema(BaseModel):
    id: int
    name: str
    seats: int
    location: str

    class Config:
        orm_mode = True


class TableCreateUpdateSchema(BaseModel):
    name: str
    seats: int
    location: str
