from typing import Optional
from pydantic import BaseModel

class Category(BaseModel):
    id:  Optional[int]
    nombre: str

    class Config:
        orm_mode = True
class CategoryUpdate(BaseModel):
    nombre: str

    class Config:
        orm_mode = True

class Respuesta(BaseModel):
    mensaje:str

class Client(BaseModel):
    #Id: Optional[int]
    name: str
    lastName: str
    document: str
    class Config:
        orm_mode = True

class User (BaseModel):
    id: int
    user: str
    password: str

    class Config:
        orm_mode = True