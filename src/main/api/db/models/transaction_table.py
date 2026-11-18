from sqlalchemy import Column, Integer, String, Float, DateTime
from src.main.api.db.base import Base

class Transaction(Base):
    __tablename__="transaction"
    id = Column(Integer, primary_key=True, autoincrement=True)
    to_account_id = Column(Integer, nullable=True)
    from_account_id = Column(Integer, nullable=True)
    credit_id = Column(Integer, nullable=True)
    amount = Column(Float)
    transaction_type = Column(String)
    created_at = Column(DateTime)


    def __repr__(self):
        return (f"<Transaction(id={self.id}, to_account_id={self.to_account_id}, \n"
                f"from_account_id={self.from_account_id}, credit_id={self.credit_id}, amount={self.amount}, \n"
                f" transaction_type={self.transaction_type}, created_at={self.created_at})>")


