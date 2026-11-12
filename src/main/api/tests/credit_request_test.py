import random, pytest

from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.credit_request import CreditRequest
from src.main.api.requests.create_account_requester import CreateAccountRequester
from src.main.api.requests.create_user_requester import CreateUserRequester
from src.main.api.requests.credit_requester import CreditRequester
from src.main.api.specs.request_specs import RequestSpecs
from src.main.api.specs.response_specs import ResponseSpecs

@pytest.mark.api
class TestCreditRequest:

    def test_credit_request_positive(self):
        username = f"Malkin{random.randint(100000, 999999)}"

        create_user_request = CreateUserRequest(username=username, password="Pas!sw0rd", role="ROLE_CREDIT_SECRET")
        CreateUserRequester(
            request_spec=RequestSpecs.auth_headers(username="admin", password="123456"),
            response_spec=ResponseSpecs.request_ok()
        ).post(create_user_request)

        # ======================= логинимся юзером ОДИН раз, заголовки используем дальше

        user_specs = RequestSpecs.auth_headers(username=username, password="Pas!sw0rd")

        # ======================= создаем счета, забираем id
        account = CreateAccountRequester(
            request_spec=user_specs,
            response_spec=ResponseSpecs.request_created()
        ).post()

        request = CreditRequest(accountId=account.id, amount=9000, termMonths=12)
        response = CreditRequester(
            request_spec=user_specs,
            response_spec=ResponseSpecs.request_created()
        ).post(request)

        assert response.balance == 9000
        assert response.creditId is not None



    @pytest.mark.parametrize("amount", [4999, 15001])
    def test_credit_request_negative(self, amount):
        username = f"Malkin{random.randint(100000, 999999)}"

        create_user_request = CreateUserRequest(username=username, password="Pas!sw0rd", role="ROLE_CREDIT_SECRET")
        CreateUserRequester(
            request_spec=RequestSpecs.auth_headers(username="admin", password="123456"),
            response_spec=ResponseSpecs.request_ok()
        ).post(create_user_request)

        # ======================= логинимся юзером ОДИН раз, заголовки используем дальше

        user_specs = RequestSpecs.auth_headers(username=username, password="Pas!sw0rd")

        # ======================= создаем счета, забираем id
        account = CreateAccountRequester(
            request_spec=user_specs,
            response_spec=ResponseSpecs.request_created()
        ).post()

        request = CreditRequest(accountId=account.id, amount=amount, termMonths=12)
        response = CreditRequester(
            request_spec=user_specs,
            response_spec=ResponseSpecs.request_bad()
        ).post(request)

        assert "Amount must be between 5000 and 15000" in response.json()["error"]
