from src.main.api.classes.api_manager import ApiManager
from src.main.api.db.crud.account_crud import AccountCrudDb as Account
from src.main.api.db.crud.credit_crud import CreditCrudDb as Credit
from src.main.api.db.crud.transaction_crud import TransactionCrudDb as Transaction
from src.main.api.models.create_account_response import CreateAccountResponse
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.credit_response import CreditResponse
from src.main.api.models.repay_request import RepayRequest
from sqlalchemy.orm import Session
import pytest


@pytest.mark.api
class TestCreditRepay:

    def test_credit_repay_positive(self, api_manager: ApiManager, create_credit_user_request: CreateUserRequest,
                                   credit: tuple[CreditResponse, CreateAccountResponse, float], db_session: Session) -> None:
        # ДОБАВИЛИ: распаковываем результат фикстуры
        response_credit, credit_account, credit_amount = credit

        repay_request = RepayRequest(
            creditId=response_credit.creditId,
            accountId=credit_account.id,
            amount=credit_amount)

        response = api_manager.user_steps.credit_repay(create_credit_user_request, repay_request)

        assert response.creditId == response_credit.creditId, \
            "ID погашенного кредита не совпадает с ожидаемым"
        assert response.amountDeposited == credit_amount, \
            "Сумма погашения не совпадает с суммой кредита"

        credit_from_db = Credit.get_credit_by_id(db_session, response_credit.creditId        )
        assert credit_from_db.balance == 0, "Кредит в БД не погашен"

        transactions = Transaction.get_transactions_by_from_account_and_type(db_session, credit_account.id,"credit_repayment")
        assert len(transactions) == 1, "Операция погашения кредита не найдена в БД"
        assert transactions[0].to_account_id is None, "У транзакции погашения кредита указан неожиданный счёт получателя"

    def test_credit_repay_negative(self, api_manager: ApiManager, create_credit_user_request: CreateUserRequest,
                                   credit: tuple[CreditResponse, CreateAccountResponse, float], db_session: Session) -> None:
        # ДОБАВИЛИ: распаковываем результат фикстуры
        response_credit, credit_account, credit_amount = credit

        # Частичное погашение запрещено
        repay_request = RepayRequest(
            creditId=response_credit.creditId,
            accountId=credit_account.id,
            amount=credit_amount / 2
        )

        response = api_manager.user_steps.credit_repay_invalid(
            create_credit_user_request,
            repay_request
        )

        assert "The amount is not enough" in response.json()["error"], \
            "При частичном погашении получено неожиданное сообщение об ошибке"

        credit_from_db = Credit.get_credit_by_id(
            db_session,
            response_credit.creditId
        )
        assert credit_from_db.balance == -credit_amount, \
            "Баланс кредита в БД изменился после отказа в частичном погашении"

        account_from_db = Account.get_account_by_id(
            db_session,
            credit_account.id
        )
        assert account_from_db.balance == credit_amount, \
            "Баланс счёта в БД изменился после отказа в частичном погашении"

