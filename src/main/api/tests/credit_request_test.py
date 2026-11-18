from src.main.api.db.crud.credit_crud import CreditCrudDb as Credit
from src.main.api.models.credit_request import CreditRequest
from sqlalchemy.orm import Session
import pytest


@pytest.mark.api
class TestCreditRequest:

    def test_credit_request_positive(self, api_manager, create_credit_user_request, db_session: Session):
        credit_account = api_manager.user_steps.create_account(create_credit_user_request)
        credit_request = CreditRequest(accountId=credit_account.id, amount=7000, termMonths=12)
        response = api_manager.user_steps.credit_request(create_credit_user_request, credit_request)

        assert response.balance == 7000
        assert response.id == credit_account.id

        credit_db = Credit.get_credit_by_id(db_session, credit_id=response.creditId)
        assert credit_db is not None
        assert credit_db.amount == 7000
        assert credit_db.account_id == credit_account.id


    @pytest.mark.parametrize("amount", [-1, 0, 4999, 15001])
    def test_credit_request_negative(self, amount, api_manager, create_credit_user_request, db_session: Session):
        credit_account = api_manager.user_steps.create_account(create_credit_user_request)
        credit_request = CreditRequest(accountId=credit_account.id, amount=amount, termMonths=12)
        response = api_manager.user_steps.credit_request_invalid(create_credit_user_request, credit_request)

        assert "Amount must be between 5000 and 15000" in response.json()["error"]

        credit_db = Credit.get_credit_by_account_id(db_session, account_id=credit_account.id)
        assert credit_db is None


