from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.requests.create_user_requester import CreateUserRequester
from src.main.api.specs.request_specs import RequestSpecs
from src.main.api.specs.response_specs import ResponseSpecs
import pytest, random

@pytest.mark.api
class TestCreateUser:

    def test_create_user_valid(self):  # ===========  создание пользователя, позитивный тест
        username = f"Malkin{random.randint(100,999)}"

        create_user_request = CreateUserRequest(username=username, password="Pas!sw0rd", role="ROLE_USER")
        response = CreateUserRequester(
            request_spect=RequestSpecs.auth_headers(username="admin", password="123456"),
            response_spec=ResponseSpecs.request_ok()
        ).post(create_user_request)

        assert create_user_request.username == response.username
        assert create_user_request.role == response.role



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
        #=============================================== создаем юзера
        create_user_request = CreateUserRequest(username=username, password=password, role="ROLE_USER")

        CreateUserRequester(
            request_spect=RequestSpecs.auth_headers(username="admin", password="123456"),
            response_spec=ResponseSpecs.request_bad()
        ).post(create_user_request)


