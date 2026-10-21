import requests, pytest, random

from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.login_user_request import LoginUserRequest
from src.main.api.models.create_account_response import CreateAccountResponse


@pytest.mark.api
class TestCreateAccount:
    def test_create_account(self):
        # ====================================== авторизуемся под админом, забираем токен
        login_user_request = LoginUserRequest(username="admin", password="123456")
        admin_response = requests.post(
            url="http://localhost:4111/api/auth/token/login",
            json=login_user_request.model_dump(),
            headers={
                "accept": "application/json",
                "Content-Type": "application/json"
            }
        )
        assert admin_response.status_code == 200
        token = admin_response.json().get("token")

        # ======================= создаем пользователя, прокинули токен админа, чтобы создать юзера
        username = f"Malkin{random.randint(100, 999)}"

        create_user_request = CreateUserRequest(username=username, password="Pas!sw0rd", role="ROLE_USER")
        user_response = requests.post(
            url="http://localhost:4111/api/admin/create",
            json=create_user_request.model_dump(),
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {token}"
            }
        )
        assert user_response.status_code == 200

        # ======================= авторизовались пользователем которого создали, взяли токен юзера
        login_user_request = LoginUserRequest(username=username, password="Pas!sw0rd")

        login_user_response = requests.post(
            url="http://localhost:4111/api/auth/token/login",
            json=login_user_request.model_dump(),
            headers={
                "accept": "application/json",
                "Content-Type": "application/json"
            }
        )
        assert login_user_response.status_code == 200
        token = login_user_response.json().get("token")

        # ======================= создаем счет для юзера с помощью его токена
        response = requests.post(
            url="http://localhost:4111/api/account/create",
            headers={
                "accept": "*/*",
                "Authorization": f"Bearer {token}",
            }

        )
        assert response.status_code == 201
        create_account_response = CreateAccountResponse(**response.json())
        assert create_account_response.balance == 0

