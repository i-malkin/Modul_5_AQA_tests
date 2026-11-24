from src.main.api.db.crud.transaction_crud import TransactionCrudDb as Transaction
from src.main.api.db.crud.account_crud import AccountCrudDb as Account
from src.main.api.generators.test_data import generate_transfer_amount
from src.main.api.models.transfer_request import TransferRequest
from sqlalchemy.orm import Session
import pytest


@pytest.mark.api
class TestTransfer:

    def test_transfer_positive(self, api_manager, create_user_request, funded_account, second_account, db_session: Session):
        account, deposit_amount = funded_account
        transfer_amount = generate_transfer_amount(deposit_amount)

        transfer_request = TransferRequest(fromAccountId=account.id,
                                           toAccountId=second_account.id,
                                           amount=transfer_amount)
        response = api_manager.user_steps.transfer(create_user_request, transfer_request)

        assert response.fromAccountId == account.id, "ID счёта отправителя в ответе не совпадает с ожидаемым"
        assert response.fromAccountIdBalance == (deposit_amount - transfer_amount), "Остаток счёта отправителя после перевода рассчитан неверно"
        assert response.toAccountId == second_account.id, "ID счёта получателя в ответе не совпадает с ожидаемым"

        sender_from_db = Account.get_account_by_id(db_session, account.id)
        assert sender_from_db.balance == (deposit_amount - transfer_amount), "Баланс счёта отправителя в БД не соответствует результату перевода"

        receiver_from_db = Account.get_account_by_id(db_session, second_account.id)
        assert receiver_from_db.balance == transfer_amount, "Баланс счёта получателя в БД не соответствует сумме перевода"

        transactions = Transaction.get_transactions_by_to_account_and_type(
            db_session, second_account.id, "transfer")
        assert len(transactions) == 1, "Операция transfer не найдена в БД"
        assert transactions[0].from_account_id == account.id, "В БД указан неверный счёт отправителя"
        assert transactions[0].amount == transfer_amount, "Сумма перевода в БД не совпадает с отправленной суммой"



    @pytest.mark.parametrize("amount, expected_error", [
        (-1, "Amount must be greater than 0"),
        (0, "Amount must be greater than 0"),
        (499, "Amount must be between 500 and 10000"),
        (10001, "Amount must be between 500 and 10000"),
    ])
    def test_transfer_negative(self, amount, expected_error, api_manager, create_user_request, funded_account,
                               second_account, db_session: Session):
        account, deposit_amount = funded_account
        transfer_request = TransferRequest(fromAccountId=account.id,
                                           toAccountId=second_account.id,
                                           amount=amount)
        response = api_manager.user_steps.transfer_invalid(create_user_request, transfer_request)

        assert expected_error in response.json()["error"], "API вернул неожиданное сообщение об ошибке"

        sender_from_db = Account.get_account_by_id(db_session, account.id)
        assert sender_from_db.balance == deposit_amount, "Баланс отправителя изменился после отклонённого перевода"

        receiver_from_db = Account.get_account_by_id(db_session, second_account.id)
        assert receiver_from_db.balance == 0, "Баланс получателя изменился после отклонённого перевода"

        transactions = Transaction.get_transactions_by_to_account_and_type(db_session, second_account.id, "transfer")
        assert len(transactions) == 0, "Операция transfer создана, хотя запрос отклонён"
