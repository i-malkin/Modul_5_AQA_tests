from src.main.api.classes.api_manager import ApiManager
from src.main.api.db.crud.transaction_crud import TransactionCrudDb as Transaction
from src.main.api.db.crud.account_crud import AccountCrudDb as Account
from src.main.api.generators.test_data import generate_deposit_amount, invalid_deposit_amounts, DEPOSIT_RANGE_ERROR
from src.main.api.models.create_account_response import CreateAccountResponse
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.deposit_request import DepositRequest
from sqlalchemy.orm import Session
import pytest


@pytest.mark.api
class TestDepositReplenishment:

    def test_deposit_replenishment_positive(self, api_manager: ApiManager,
                                            create_user_request: CreateUserRequest,
                                            account: CreateAccountResponse, db_session: Session) -> None:
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



    @pytest.mark.parametrize("amount", invalid_deposit_amounts())
    def test_deposit_replenishment_negative(self, amount: float, api_manager: ApiManager,
                                            create_user_request: CreateUserRequest,
                                            account: CreateAccountResponse, db_session: Session) -> None:
        deposit_request = DepositRequest(accountId=account.id, amount=amount)
        response = api_manager.user_steps.deposit_invalid(create_user_request, deposit_request)

        assert DEPOSIT_RANGE_ERROR in response.json()["error"], \
            "При некорректной сумме пополнения API вернул неожиданную ошибку"

        account_from_db = Account.get_account_by_id(db_session, account.id)
        assert account_from_db.balance == 0, "Баланс счёта изменился после отклонённого пополнения"

        transactions = Transaction.get_transactions_by_to_account_and_type(db_session, account.id, "deposit")
        assert len(transactions) == 0, "Транзакция deposit появилась в БД, хотя запрос был отклонён"