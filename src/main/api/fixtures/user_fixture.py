from src.main.api.generators.model_generator import RandomModelGenerator
from src.main.api.models.create_user_request import CreateUserRequest, UserRole
from src.main.api.classes.api_manager import ApiManager
import pytest


@pytest.fixture
def create_user_request(api_manager: ApiManager) -> CreateUserRequest:
    user_request = RandomModelGenerator.generate(CreateUserRequest)
    api_manager.admin_steps.create_user(user_request)
    return user_request

@pytest.fixture
def create_credit_user_request(api_manager: ApiManager) -> CreateUserRequest:
    user_request = RandomModelGenerator.generate(CreateUserRequest)
    user_request.role = UserRole.CREDIT_SECRET
    api_manager.admin_steps.create_user(user_request)
    return user_request

