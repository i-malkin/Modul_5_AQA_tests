from sqlalchemy import Column, Integer, String, Float, DateTime
from src.main.api.db.base import Base


class Credit(Base):
    __tablename__="credit"
    id = Column(Integer, primary_key=True, autoincrement=True)
    account_id = Column(Integer)
    amount = Column(Float)
    term_months = Column(Integer)
    balance = Column(Float)
    created_at = Column(DateTime)

    def __repr__(self):
        return (f"<Credit(id={self.id}, account_id={self.account_id}, amount={self.amount}, \n"
                f"term_months={self.term_months}, balance={self.balance}, created_at={self.created_at})>")