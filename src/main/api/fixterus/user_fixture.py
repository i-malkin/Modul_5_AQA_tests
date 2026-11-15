from src.main.api.models.create_user_request import CreateUserRequest
import pytest


@pytest.fixture
def create_user_request(api_manager):
    user_request = CreateUserRequest(username="Vladivostok2003", password="Pas!sw0rd", role="ROLE_USER")
    api_manager.admin_steps.create_user(user_request)
    return user_request

