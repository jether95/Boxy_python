from .Database import Base
from sqlalchemy import Column, String, Integer

class Category(Base):
    __tablename__ = 'Category'
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(50))
