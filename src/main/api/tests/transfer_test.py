from src.main.api.db.crud.transaction_crud import TransactionCrudDb as Transaction
from src.main.api.db.crud.account_crud import AccountCrudDb as Account
from src.main.api.models.transfer_request import TransferRequest
from src.main.api.models.deposit_request import DepositRequest
from sqlalchemy.orm import Session
import pytest


@pytest.mark.api
class TestTransfer:

    def test_transfer_positive(self, api_manager, create_user_request, account,
                               second_account, db_session: Session):
        deposit_amount = 6000
        transfer_amount = 500
        deposit_request = DepositRequest(accountId=account.id, amount=deposit_amount)
        api_manager.user_steps.deposit(create_user_request, deposit_request)

        transfer_request = TransferRequest(fromAccountId=account.id,
                                           toAccountId=second_account.id,
                                           amount=transfer_amount)
        response = api_manager.user_steps.transfer(create_user_request, transfer_request)

        assert response.fromAccountId == account.id
        assert response.fromAccountIdBalance == (deposit_amount - transfer_amount)
        assert response.toAccountId == second_account.id

        sender_from_db = Account.get_account_by_id(db_session, account.id)
        assert sender_from_db.balance == (deposit_amount - transfer_amount)

        receiver_from_db = Account.get_account_by_id(db_session, second_account.id)
        assert receiver_from_db.balance == transfer_amount

        transactions = Transaction.get_transactions_by_to_account_and_type(db_session, second_account.id,
                                                                           "transfer")
        assert len(transactions) == 1, "Операция transfer не найдена в БД"
        assert transactions[0].from_account_id == account.id
        assert transactions[0].amount == transfer_amount



    @pytest.mark.parametrize("amount, expected_error", [
        (-1, "Amount must be greater than 0"),
        (0, "Amount must be greater than 0"),
        (499, "Amount must be between 500 and 10000"),
        (10001, "Amount must be between 500 and 10000"),
    ])
    def test_transfer_negative(self, amount, expected_error, api_manager, create_user_request,
                               account, second_account, db_session: Session):
        deposit_amount = 8000
        deposit_request = DepositRequest(accountId=account.id, amount=deposit_amount)
        api_manager.user_steps.deposit(create_user_request, deposit_request)

        transfer_request = TransferRequest(fromAccountId=account.id,
                                           toAccountId=second_account.id,
                                           amount=amount)
        response = api_manager.user_steps.transfer_invalid(create_user_request, transfer_request)

        assert expected_error in response.json()["error"]

        sender_from_db = Account.get_account_by_id(db_session, account.id)
        assert sender_from_db.balance == deposit_amount

        receiver_from_db = Account.get_account_by_id(db_session, second_account.id)
        assert receiver_from_db.balance == 0

        transactions = Transaction.get_transactions_by_to_account_and_type(db_session, second_account.id,
                                                                           "transfer")
        assert len(transactions) == 0, "Операция transfer создана, хотя запрос отклонён"
