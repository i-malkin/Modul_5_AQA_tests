import pytest, random

from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.deposit_request import DepositRequest
from src.main.api.requests.create_account_requester import CreateAccountRequester
from src.main.api.requests.create_user_requester import CreateUserRequester
from src.main.api.requests.deposit_requester import DepositRequester
from src.main.api.specs.request_specs import RequestSpecs
from src.main.api.specs.response_specs import ResponseSpecs


@pytest.mark.api
class TestDepositReplenishment:  # ===== тест пополнения баланса

    def test_deposit_replenishment_positive(self):
        # ======================= создаем юзера (под админом)
        username = f"Malkin{random.randint(100, 999)}"

        create_user_request = CreateUserRequest(username=username, password="Pas!sw0rd", role="ROLE_USER")
        CreateUserRequester(
            request_spect=RequestSpecs.auth_headers(username="admin", password="123456"),
            response_spec=ResponseSpecs.request_ok()
        ).post(create_user_request)

        # ======================= логинимся юзером ОДИН раз, заголовки используем дальше
        user_specs = RequestSpecs.auth_headers(username=username, password="Pas!sw0rd")

        # ======================= создаем счет, забираем его id
        account = CreateAccountRequester(
            request_spect=user_specs,
            response_spec=ResponseSpecs.request_created()
        ).post()

        # ======================= пополняем счет
        deposit_request = DepositRequest(accountId=account.id, amount=2500.5)
        response = DepositRequester(
            request_spect=user_specs,
            response_spec=ResponseSpecs.request_ok()
        ).post(deposit_request)

        assert response.id == account.id
        assert response.balance == 2500.5




    @pytest.mark.parametrize("amount", [-100, 0, 999, 9001])
    def test_deposit_replenishment_negative(self, amount):
        username = f"Malkin{random.randint(100, 999)}"
        create_user_request = CreateUserRequest(username=username, password="Pas!sw0rd", role="ROLE_USER")
        CreateUserRequester(
            request_spect=RequestSpecs.auth_headers(username="admin", password="123456"),
            response_spec=ResponseSpecs.request_ok()
        ).post(create_user_request)

        user_specs = RequestSpecs.auth_headers(username=username, password="Pas!sw0rd")

        account = CreateAccountRequester(
            request_spect=user_specs,
            response_spec=ResponseSpecs.request_created()
        ).post()

        deposit_request = DepositRequest(accountId=account.id, amount=amount)
        # спека проверяет статус 400, а requester вернет сырой Response (не модель)
        response = DepositRequester(
            request_spect=user_specs,
            response_spec=ResponseSpecs.request_bad()
        ).post(deposit_request)

        assert "Amount must be between 1000 and 9000" in response.json()["error"]