from src.main.api.models.credit_request import CreditRequest
import pytest



@pytest.fixture
def credit(api_manager, create_credit_user_request):
    credit_account = api_manager.user_steps.create_account(create_credit_user_request)

    credit_request = CreditRequest(accountId=credit_account.id, amount=7800, termMonths=12)
    response = api_manager.user_steps.credit_request(create_credit_user_request, credit_request)

    return response