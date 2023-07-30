from pydantic import BaseModel

class Category(BaseModel):
    id: int
    nombre: str

    class Config:
        orm_mode = True
class Client(BaseModel):
    Id: int
    name: str
    lastName: str
    document: str
    class Config:
        orm_mode = True