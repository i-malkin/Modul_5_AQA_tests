from src.main.api.classes.api_manager import ApiManager
from typing import List, Any
import pytest

@pytest.fixture
def api_manager(created_obj: List[Any]) -> ApiManager:
    return ApiManager(created_obj)

