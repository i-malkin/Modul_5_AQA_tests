from src.main.api.db.models.transaction_table import Transaction
from sqlalchemy.orm import Session


class TransactionCrudDb:
    @staticmethod
    def get_transactions_by_to_account_and_type(db: Session, account_id: int, transaction_type: str) -> list[type[Transaction]]:
        return db.query(Transaction).filter_by(to_account_id=account_id, transaction_type=transaction_type).all()

    @staticmethod
    def get_transactions_by_from_account_and_type(db: Session, account_id: int, transaction_type: str) -> list[type[Transaction]]:
        return db.query(Transaction).filter_by(from_account_id=account_id, transaction_type=transaction_type).all()
