from src.main.api.classes.api_manager import ApiManager
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.login_user_request import LoginUserRequest
import pytest


@pytest.mark.api
class TestUserLogin:
    def test_login_admin(self, api_manager: ApiManager) -> None:
        login_user_request = LoginUserRequest(username="admin", password="123456")
        response = api_manager.admin_steps.login_user(login_user_request)

        assert login_user_request.username == response.user.username, "Username администратора в ответе не совпадает с отправленным"
        assert response.user.role == "ROLE_ADMIN",  "У авторизованного администратора неверная роль"


    def test_login_user(self, api_manager: ApiManager, create_user_request: CreateUserRequest) -> None:
        response = api_manager.admin_steps.login_user(create_user_request)

        assert create_user_request.username == response.user.username, "Username пользователя в ответе не совпадает с отправленным"
        assert response.user.role == "ROLE_USER",    "У авторизованного пользователя неверная роль"

