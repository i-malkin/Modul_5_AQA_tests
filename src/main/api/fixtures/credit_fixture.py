
import pytest
from src.main.api.classes.api_manager import ApiManager
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.credit_response import CreditResponse
from src.main.api.models.create_account_response import CreateAccountResponse
from src.main.api.models.credit_request import CreditRequest
from src.main.api.generators.test_data import generate_credit_amount


@pytest.fixture
def credit(
    api_manager: ApiManager,
    create_credit_user_request: CreateUserRequest
) -> tuple[CreditResponse, CreateAccountResponse, float]:

    credit_amount = generate_credit_amount()

    # Создаём счёт — предусловие для оформления кредита
    credit_account = api_manager.user_steps.create_account(
        create_credit_user_request
    )

    credit_request = CreditRequest(
        accountId=credit_account.id,
        amount=credit_amount,
        termMonths=12
    )

    response = api_manager.user_steps.credit_request(
        create_credit_user_request,
        credit_request
    )

    # Возвращаем ответ и сумму, чтобы тест мог проверить результат
    return response, credit_account, credit_amount
