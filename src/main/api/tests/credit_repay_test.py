from src.main.api.db.crud.account_crud import AccountCrudDb as Account
from src.main.api.db.crud.credit_crud import CreditCrudDb as Credit
from src.main.api.db.crud.transaction_crud import TransactionCrudDb as Transaction
from src.main.api.models.repay_request import RepayRequest
from sqlalchemy.orm import Session
import pytest


@pytest.mark.api
class TestCreditRepay:

    def test_credit_repay_positive(self, api_manager, create_credit_user_request, credit, db_session: Session):
        repay_request = RepayRequest(creditId=credit.creditId,
                                     accountId=credit.id,
                                     amount=credit.amount)
        response = api_manager.user_steps.credit_repay(create_credit_user_request, repay_request)

        assert response.creditId == credit.creditId
        assert response.amountDeposited == credit.amount

        credit_from_db = Credit.get_credit_by_id(db_session, credit.creditId)
        assert credit_from_db.balance == 0, "Кредит в БД не погашен"

        transactions = Transaction.get_transactions_by_from_account_and_type(db_session, credit.id, "credit_repayment")
        assert len(transactions) == 1
        assert transactions[0].to_account_id is None

    def test_credit_repay_negative(self, api_manager, create_credit_user_request, credit, db_session: Session):
        # частичное погашение запрещено
        repay_request = RepayRequest(creditId=credit.creditId,
                                     accountId=credit.id,
                                     amount=(credit.amount / 2))
        response = api_manager.user_steps.credit_repay_invalid(create_credit_user_request, repay_request)

        assert "The amount is not enough" in response.json()["error"]

        credit_from_db = Credit.get_credit_by_id(db_session, credit.creditId)
        assert credit_from_db.balance == -credit.amount, "Баланс кредита в БД изменился после отказа"

        account_from_db = Account.get_account_by_id(db_session, credit.id)
        assert account_from_db.balance == credit.amount, "Баланс счёта в БД изменился после отказа"

