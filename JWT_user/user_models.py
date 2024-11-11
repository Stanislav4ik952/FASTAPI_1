from sqlalchemy import Column, Integer, String
from database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    users_id = Column(Integer, unique=True, index=True)
    login = Column(String, unique=True, index=True)
    hashed_password = Column(String)
