from app.Database import Base
from sqlalchemy import Column, Integer, String
class User(Base):
    __tablename__ = 'User'
    id = Column(Integer, primary_key=True, index=True)
    user = Column(String(100))
    password = Column(String(100))
