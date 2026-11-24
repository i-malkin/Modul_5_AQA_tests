from requests import Response

from src.main.api.classes.api_manager import ApiManager
from src.main.api.db.crud.credit_crud import CreditCrudDb as Credit
from src.main.api.models.create_account_response import CreateAccountResponse
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.credit_request import CreditRequest
from sqlalchemy.orm import Session
import pytest

from src.main.api.models.credit_response import CreditResponse


@pytest.mark.api
class TestCreditRequest:

    def test_credit_request_positive(self, credit: tuple[CreditResponse, CreateAccountResponse, float],
                                     db_session: Session) -> None:
        response: CreditResponse
        response, credit_account, credit_amount = credit

        assert response.balance == credit_amount, "Баланс в ответе API не совпадает с суммой оформленного кредита"
        assert response.id == credit_account.id, "ID счёта в ответе API не совпадает с созданным счётом"

        credit_db = Credit.get_credit_by_id(db_session, credit_id=response.creditId)
        assert credit_db is not None, "Запись о кредите отсутствует в БД"
        assert credit_db.amount == credit_amount, "Сумма кредита в БД не совпадает с суммой запроса"
        assert credit_db.account_id == credit_account.id, "Кредит привязан к неверному счёту в БД"


    @pytest.mark.parametrize("amount", [-1, 0, 4999, 15001])
    def test_credit_request_negative(self, amount: int, api_manager: ApiManager,
                                     create_credit_user_request: CreateUserRequest, db_session: Session) -> None:
        credit_account = api_manager.user_steps.create_account(create_credit_user_request)
        credit_request = CreditRequest(accountId=credit_account.id, amount=amount, termMonths=12)
        response: Response = api_manager.user_steps.credit_request_invalid(create_credit_user_request, credit_request)

        assert "Amount must be between 5000 and 15000" in response.json()["error"], f"Для некорректной суммы {amount} не получена ожидаемая ошибка"

        credit_db = Credit.get_credit_by_account_id(db_session, account_id=credit_account.id)
        assert credit_db is None, f"Для некорректной суммы {amount} в БД не должно быть создано записи о кредите"


