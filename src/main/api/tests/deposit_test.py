from src.main.api.db.crud.transaction_crud import TransactionCrudDb as Transaction
from src.main.api.db.crud.account_crud import AccountCrudDb as Account
from src.main.api.generators.test_data import generate_deposit_amount
from src.main.api.models.deposit_request import DepositRequest
from sqlalchemy.orm import Session
import pytest


@pytest.mark.api
class TestDepositReplenishment:

    def test_deposit_replenishment_positive(self, api_manager, create_user_request, account, db_session: Session) -> None:
        amount = generate_deposit_amount()
        deposit_request = DepositRequest(accountId=account.id, amount=amount)
        response = api_manager.user_steps.deposit(create_user_request, deposit_request)

        assert response.id == account.id, "ID счёта в ответе не совпадает с ID созданного счёта"
        assert response.balance == amount, "Баланс в ответе API не совпадает с суммой пополнения"

        account_from_db = Account.get_account_by_id(db_session, account.id)
        assert account_from_db.balance == amount, "Баланс в БД не совпадает с суммой пополнения"

        transactions = Transaction.get_transactions_by_to_account_and_type(db_session, account.id, "deposit")
        assert len(transactions) == 1, "Операция deposit не найдена в БД"
        assert transactions[0].amount == amount,  "Сумма транзакции в БД не совпадает с суммой пополнения"
        assert transactions[0].from_account_id is None,  "У операции deposit не должен быть указан счёт отправителя"



    @pytest.mark.parametrize("amount", [-100, 0, 999, 9001])
    def test_deposit_replenishment_negative(self, amount, api_manager, create_user_request, account, db_session: Session) -> None:
        deposit_request = DepositRequest(accountId=account.id, amount=amount)
        response = api_manager.user_steps.deposit_invalid(create_user_request, deposit_request)

        assert "Amount must be between 1000 and 9000" in response.json()["error"]

        account_from_db = Account.get_account_by_id(db_session, account.id)
        assert account_from_db.balance == 0, "Баланс счета должен быть равен нулю"

        transactions = Transaction.get_transactions_by_to_account_and_type(db_session, account.id, "deposit")
        assert len(transactions) == 0, "Операция deposit создана, хотя запрос отклонён"