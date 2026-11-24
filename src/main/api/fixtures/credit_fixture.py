from src.main.api.classes.api_manager import ApiManager
from src.main.api.generators.test_data import generate_credit_amount, CREDIT_TERM_MONTHS
from src.main.api.models.create_account_response import CreateAccountResponse
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.credit_request import CreditRequest
from src.main.api.models.credit_response import CreditResponse
import pytest


@pytest.fixture
def credit_account(api_manager: ApiManager,
                   create_credit_user_request: CreateUserRequest) -> CreateAccountResponse:

    return api_manager.user_steps.create_account(create_credit_user_request)


@pytest.fixture
def credit_request(credit_account: CreateAccountResponse) -> CreditRequest:
    return CreditRequest(
        accountId=credit_account.id,
        amount=generate_credit_amount(),
        termMonths=CREDIT_TERM_MONTHS
    )


@pytest.fixture
def credit(
    api_manager: ApiManager,
    create_credit_user_request: CreateUserRequest,
    credit_account: CreateAccountResponse,
    credit_request: CreditRequest
) -> tuple[CreditResponse, CreateAccountResponse, float]:
    response = api_manager.user_steps.credit_request(create_credit_user_request, credit_request)

    return response, credit_account, credit_request.amount     # ответ, счёт и сумма
