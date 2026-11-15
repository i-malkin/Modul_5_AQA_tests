from src.main.api.generators.model_generator import RandomModelGenerator
from src.main.api.models.create_user_request import CreateUserRequest
import pytest

@pytest.mark.api
class TestCreateUser:

    @pytest.mark.parametrize(
        "create_user_request",
        [RandomModelGenerator.generate(CreateUserRequest)],
    )
    def test_create_user_valid(self, api_manager, create_user_request):
        response = api_manager.admin_steps.create_user(create_user_request)

        assert create_user_request.username == response.username
        assert create_user_request.role == response.role


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
    def test_create_user_invalid(self, username, password, api_manager):
        create_user_request = CreateUserRequest(username=username, password=password, role="ROLE_USER")

        api_manager.admin_steps.create_invalid_user(create_user_request)


