from pydantic import BaseModel

class Category(BaseModel):
    id: int
    nombre: str

    class Config:
        orm_mode = True