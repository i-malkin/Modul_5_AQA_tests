import pytest, random

from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.credit_request import CreditRequest
from src.main.api.models.repay_request import RepayRequest
from src.main.api.requests.create_account_requester import CreateAccountRequester
from src.main.api.requests.create_user_requester import CreateUserRequester
from src.main.api.requests.credit_requester import CreditRequester
from src.main.api.requests.repay_requester import RepayRequester
from src.main.api.specs.request_specs import RequestSpecs
from src.main.api.specs.response_specs import ResponseSpecs

@pytest.mark.api
class TestCreditRepay:

    def test_credit_repay_positive(self):
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

        request_credit = CreditRequest(accountId=account.id, amount=10000, termMonths=12)
        response_credit = CreditRequester(
            request_spec=user_specs,
            response_spec=ResponseSpecs.request_created()
        ).post(request_credit)

        credit_id = response_credit.creditId
        request_repay = RepayRequest(creditId=credit_id, accountId=account.id, amount=10000)
        response_repay = RepayRequester(
            request_spec=user_specs,
            response_spec=ResponseSpecs.request_ok()
        ).post(request_repay)

        assert response_repay.creditId == credit_id
        assert response_repay.amountDeposited == 10000



    def test_credit_repay_negative(self):
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

        request_credit = CreditRequest(accountId=account.id, amount=10000, termMonths=12)
        response_credit = CreditRequester(
            request_spec=user_specs,
            response_spec=ResponseSpecs.request_created()
        ).post(request_credit)

        credit_id = response_credit.creditId
        request_repay = RepayRequest(creditId=credit_id, accountId=account.id, amount=5000)
        response_repay = RepayRequester(
            request_spec=user_specs,
            response_spec=ResponseSpecs.request_unprocessable()
        ).post(request_repay)

        assert "The amount is not enough" in response_repay.json()["error"]


