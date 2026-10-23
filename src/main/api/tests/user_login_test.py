import pytest, random
from src.main.api.models.login_user_request import LoginUserRequest
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.requests.create_user_requester import CreateUserRequester
from src.main.api.requests.login_user_requester import LoginUserRequester
from src.main.api.specs.request_specs import RequestSpecs
from src.main.api.specs.response_specs import ResponseSpecs


@pytest.mark.api
class TestUserLogin:
    # ====================================== тест авторизации под админом
    def test_login_admin(self):
        login_user_request = LoginUserRequest(username="admin", password="123456")

        response = LoginUserRequester(
            request_spect=RequestSpecs.unauth_headers(),
            response_spec=ResponseSpecs.request_ok()
        ).post(login_user_request)

        assert login_user_request.username == response.user.username
        assert response.user.role == "ROLE_ADMIN"



    def test_login_user(self):  #===== тест создания пользователя
        username = f"Malkin{random.randint(100, 999)}"
        create_user_request = CreateUserRequest(username=username, password="Pas!sw0rd", role="ROLE_USER")

        CreateUserRequester(
            request_spect=RequestSpecs.auth_headers(username="admin", password="123456"),
            response_spec=ResponseSpecs.request_ok()
        ).post(create_user_request)


        login_user_request = LoginUserRequest(username=username, password="Pas!sw0rd")

        response = LoginUserRequester(
            request_spect=RequestSpecs.unauth_headers(),
            response_spec=ResponseSpecs.request_ok()
        ).post(login_user_request)

        assert login_user_request.username == response.user.username
        assert response.user.role == "ROLE_USER"
