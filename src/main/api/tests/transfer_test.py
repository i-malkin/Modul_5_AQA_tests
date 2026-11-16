from src.main.api.models.transfer_request import TransferRequest
from src.main.api.models.deposit_request import DepositRequest
import pytest


@pytest.mark.senior
class TestTransfer:

    def test_transfer_positive(self, api_manager, create_user_request, account, second_account):
        deposit_request = DepositRequest(accountId=account.id, amount=4500)
        api_manager.user_steps.deposit(create_user_request, deposit_request)

        transfer_request = TransferRequest(fromAccountId=account.id,
                                           toAccountId=second_account.id,
                                           amount=500)
        response = api_manager.user_steps.transfer(create_user_request, transfer_request)

        assert response.fromAccountId == account.id
        assert response.fromAccountIdBalance == 4000
        assert response.toAccountId == second_account.id



    @pytest.mark.parametrize("amount, expected_error", [
        (-1, "Amount must be greater than 0"),
        (0, "Amount must be greater than 0"),
        (499, "Amount must be between 500 and 10000"),
        (10001, "Amount must be between 500 and 10000"),
    ])
    def test_transfer_negative(self, amount, expected_error, api_manager, create_user_request, account, second_account):
        deposit_request = DepositRequest(accountId=account.id, amount=8000)
        api_manager.user_steps.deposit(create_user_request, deposit_request)

        transfer_request = TransferRequest(fromAccountId=account.id,
                                           toAccountId=second_account.id,
                                           amount=amount)
        response = api_manager.user_steps.transfer_invalid(create_user_request, transfer_request)

        assert expected_error in response.json()["error"]