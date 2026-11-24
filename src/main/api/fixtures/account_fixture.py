from src.main.api.models.deposit_request import DepositRequest
from src.main.api.models.create_account_response import CreateAccountResponse
from src.main.api.generators.test_data import generate_deposit_amount
import pytest

@pytest.fixture
def account(api_manager, create_user_request):
    return api_manager.user_steps.create_account(create_user_request)

@pytest.fixture
def second_account(api_manager, create_user_request):
    return api_manager.user_steps.create_account(create_user_request)

@pytest.fixture
def funded_account(api_manager, create_user_request, account) -> tuple[CreateAccountResponse, float]:
    # ИЗМЕНИЛИ: подготовка счёта теперь находится в фикстуре
    deposit_amount = generate_deposit_amount()

    deposit_request = DepositRequest(
        accountId=account.id,
        amount=deposit_amount
    )

    api_manager.user_steps.deposit(create_user_request, deposit_request)

    # Возвращаем счёт и сумму, на которую его пополнили
    return account, deposit_amount