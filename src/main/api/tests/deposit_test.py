from src.main.api.models.deposit_request import DepositRequest
import pytest


@pytest.mark.api
class TestDepositReplenishment:

    def test_deposit_replenishment_positive(self, api_manager, create_user_request, account):
        deposit_request = DepositRequest(accountId=account.id, amount=2500.5)
        response = api_manager.user_steps.deposit(create_user_request, deposit_request)

        assert response.id == account.id
        assert response.balance == 2500.5




    @pytest.mark.parametrize("amount", [-100, 0, 999, 9001])
    def test_deposit_replenishment_negative(self, amount, api_manager, create_user_request, account):
        deposit_request = DepositRequest(accountId=account.id, amount=amount)
        response = api_manager.user_steps.deposit_invalid(create_user_request, deposit_request)

        assert "Amount must be between 1000 and 9000" in response.json()["error"]