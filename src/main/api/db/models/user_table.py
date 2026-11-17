from sqlalchemy import Column, Integer, String, DateTime
from src.main.api.db.base import Base

class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, unique=True, nullable=True)
    password = Column(String, nullable=True)
    role = Column(String, nullable=True)
    deleted_at = Column(DateTime, nullable=True)

    def __repr__(self):
        return f"<User(id={self.id}, username={self.username}, role={self.role}, deleted_at={self.deleted_at})>"





