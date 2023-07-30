from .Database import Base
from sqlalchemy import Column, String, Integer
class Client(Base):
    __tablename__ = 'Client'
    Id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50))
    lastName = Column(String(50))
    document = Column(String(30))
