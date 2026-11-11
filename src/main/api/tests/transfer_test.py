import pytest, random

from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.deposit_request import DepositRequest
from src.main.api.models.transfer_request import TransferRequest
from src.main.api.requests.create_account_requester import CreateAccountRequester
from src.main.api.requests.create_user_requester import CreateUserRequester
from src.main.api.requests.deposit_requester import DepositRequester
from src.main.api.requests.transfer_requester import TransferRequester
from src.main.api.specs.request_specs import RequestSpecs
from src.main.api.specs.response_specs import ResponseSpecs


@pytest.mark.api
class TestTransfer:

    def test_transfer_positive(self):
        # ======================= создаем юзера (под админом)
        username = f"Malkin{random.randint(100, 999)}"

        create_user_request = CreateUserRequest(username=username, password="Pas!sw0rd", role="ROLE_USER")
        CreateUserRequester(
            request_spec
            =RequestSpecs.auth_headers(username="admin", password="123456"),
            response_spec=ResponseSpecs.request_ok()
        ).post(create_user_request)

        # ======================= логинимся юзером ОДИН раз, заголовки используем дальше
        user_specs = RequestSpecs.auth_headers(username=username, password="Pas!sw0rd")

        # ======================= создаем 2 счета, забираем их id и пополняем
        account_1 = CreateAccountRequester(
            request_spec
            =user_specs,
            response_spec=ResponseSpecs.request_created()
        ).post()

        account_2 = CreateAccountRequester(
            request_spec
            =user_specs,
            response_spec=ResponseSpecs.request_created()
        ).post()

        deposit_request = DepositRequest(accountId=account_1.id, amount=4500)
        DepositRequester(
            request_spec
            =user_specs,
            response_spec=ResponseSpecs.request_ok()
        ).post(deposit_request)

        transfer_request = TransferRequest(fromAccountId=account_1.id, toAccountId=account_2.id, amount=500)
        response=TransferRequester(
            request_spec
            =user_specs,
            response_spec=ResponseSpecs.request_ok()
        ).post(transfer_request)

        assert response.fromAccountId == account_1.id
        assert response.fromAccountIdBalance == 4000


    @pytest.mark.parametrize("amount, expected_error", [
        (-1, "Amount must be greater than 0"),
        (0, "Amount must be greater than 0"),
        (499, "Amount must be between 500 and 10000"),
        (10001, "Amount must be between 500 and 10000"),
    ])
    def test_transfer_negative(self, amount, expected_error):
        # ======================= создаем юзера (под админом)
        username = f"Malkin{random.randint(100, 999)}"

        create_user_request = CreateUserRequest(username=username, password="Pas!sw0rd", role="ROLE_USER")
        CreateUserRequester(
            request_spec
            =RequestSpecs.auth_headers(username="admin", password="123456"),
            response_spec=ResponseSpecs.request_ok()
        ).post(create_user_request)

        # ======================= логинимся юзером ОДИН раз, заголовки используем дальше
        user_specs = RequestSpecs.auth_headers(username=username, password="Pas!sw0rd")

        # ======================= создаем 2 счета, забираем их id и пополняем
        account_1 = CreateAccountRequester(
            request_spec
            =user_specs,
            response_spec=ResponseSpecs.request_created()
        ).post()

        account_2 = CreateAccountRequester(
            request_spec
            =user_specs,
            response_spec=ResponseSpecs.request_created()
        ).post()

        deposit_request = DepositRequest(accountId=account_1.id, amount=8000)
        DepositRequester(
            request_spec
            =user_specs,
            response_spec=ResponseSpecs.request_ok()
        ).post(deposit_request)

        transfer_request = TransferRequest(fromAccountId=account_1.id, toAccountId=account_2.id, amount=amount)
        response=TransferRequester(
            request_spec
            =user_specs,
            response_spec=ResponseSpecs.request_bad()
        ).post(transfer_request)

        assert expected_error in response.json()["error"]