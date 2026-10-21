import requests, pytest, random

from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.create_user_response import CreateUserResponse
from src.main.api.models.login_user_request import LoginUserRequest


@pytest.mark.api
class TestCreateUser:
    def test_create_user_valid(self):  # ===========  создание пользователя, позитивный тест
        # ================================ авторизуемся под админом чтобы создать пользователя

        login_user_request = LoginUserRequest(username="admin", password="123456")

        login_admin_response = requests.post(
            url="http://localhost:4111/api/auth/token/login",
            json=login_user_request.model_dump(),
            headers={
                "accept" : "application/json",
                "Content-Type" : "application/json"
                }
        )
        assert login_admin_response.status_code == 200
        token = login_admin_response.json().get("token")

        # ==================================================== создаем юзера
        #username = f"Malkin{random.randint(100,999)}"

        create_user_request = CreateUserRequest(username="Max123", password="Pas!sw0rd", role="ROLE_USER")
        response = requests.post(
            url="http://localhost:4111/api/admin/create",
            json=create_user_request.model_dump(),
            headers={
                "Content-Type" : "application/json",
                "Authorization": f"Bearer {token}"
            }
        )
        assert response.status_code == 200
        create_user_response = CreateUserResponse(**response.json())
        assert create_user_request.username == create_user_response.username
        assert create_user_request.role == create_user_response.role

    # ===================================== негативные тесты на создание пользователя через параметризацию
    @pytest.mark.parametrize(
        "username, password",
        [
            ("абв","Pas!sw0rd"),
            ("ab", "Pas!sw0rd"),
            ("abc!", "Pas!sw0rd"),
            ("Max1", "Pas!sw0rд"),
            ("Max2", "Pas!sw0"),
            ("Max3", "pas!sw0rd"),
            ("Max4", "PAS!SW0RD"),
            ("Max5", "PASSSWORD"),
            ("Max6", "PAS!SWRRD"),
        ]
    )
    def test_create_user_invalid(self, username, password):
        #============================= авторизация под админом чтобы были права создать юзера
        login_admin_response = requests.post(
            url="http://localhost:4111/api/auth/token/login",
            json={
                "username": "admin",
                "password": "123456"
            },
            headers={
                "accept": "application/json",
                "Content-Type": "application/json"
            }
        )
        token = login_admin_response.json().get("token")

        #=============================================== создаем самого юзера
        create_user_response = requests.post(
            url="http://localhost:4111/api/admin/create",
            json={
                "username": username,
                "password": password,
                "role": "ROLE_USER"
            },
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {token}"
            }
        )

        assert create_user_response.status_code == 400
