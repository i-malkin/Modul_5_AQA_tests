import pytest

@pytest.fixture
def account(api_manager, create_user_request):
    return api_manager.user_steps.create_account(create_user_request)

@pytest.fixture
def second_account(api_manager, create_user_request):
    return api_manager.user_steps.create_account(create_user_request)

