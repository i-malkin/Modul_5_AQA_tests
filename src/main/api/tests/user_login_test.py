import requests, pytest, random
from src.main.api.models.login_user_request import LoginUserRequest
from src.main.api.models.login_user_response import LoginUserResponse
from src.main.api.models.create_user_request import CreateUserRequest

@pytest.mark.api
class TestUserLogin:
    # ====================================== тест авторизации под админом
    def test_login_admin(self):
        login_user_request = LoginUserRequest(username="admin", password="123456")

        response = requests.post(
            url="http://localhost:4111/api/auth/token/login",
            json=login_user_request.model_dump(),
            headers={
                "accept": "application/json",
                "Content-Type": "application/json"
            }
        )
        assert response.status_code == 200
        login_user_response = LoginUserResponse(**response.json())

        assert login_user_request.username == login_user_response.user.username
        assert login_user_response.user.role == "ROLE_ADMIN"




    def test_login_user(self):  #===== тест создания пользователя
        # ====================================== авторизуемся под админом
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

        # ====================================== создаем пользователя
        username = f"Malkin{random.randint(100, 999)}"
        create_user_request = CreateUserRequest(username=username, password="Pas!sw0rd", role="ROLE_USER")

        create_user_response = requests.post(
            url="http://localhost:4111/api/admin/create",
            json=create_user_request.model_dump(),
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {token}"
            }
        )
        assert create_user_response.status_code == 200

        login_user_request = LoginUserRequest(username=username, password="Pas!sw0rd")
        response = requests.post(
            url="http://localhost:4111/api/auth/token/login",
            json=login_user_request.model_dump(),
            headers={
                "accept": "application/json",
                "Content-Type": "application/json"
            }
        )

        assert response.status_code == 200
        login_admin_response = LoginUserResponse(**response.json())

        assert login_user_request.username == login_admin_response.user.username
        assert login_admin_response.user.role == "ROLE_USER"
