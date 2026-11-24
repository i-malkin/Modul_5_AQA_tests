from src.main.api.classes.api_manager import ApiManager
from src.main.api.generators.model_generator import RandomModelGenerator
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.db.crud.user_crud import UserCrudDb as User
from sqlalchemy.orm import Session
import pytest

@pytest.mark.api
class TestCreateUser:

    @pytest.mark.parametrize("create_user_request", [RandomModelGenerator.generate(CreateUserRequest)])
    def test_create_user_valid(self, api_manager: ApiManager, create_user_request: CreateUserRequest, db_session: Session) -> None:
        response = api_manager.admin_steps.create_user(create_user_request)

        assert create_user_request.username == response.username, "Username созданного пользователя не совпадает с отправленным"
        assert create_user_request.role == response.role,  "Роль созданного пользователя не совпадает с указанной в запросе"

        user_from_db = User.get_user_by_username(db_session, create_user_request.username)
        assert user_from_db.username == create_user_request.username, "Созданного пользователя нет в БД"

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
    def test_create_user_invalid(self, username: str, password: str, api_manager: ApiManager, db_session: Session) -> None:
        create_user_request = CreateUserRequest(username=username, password=password, role="ROLE_USER")
        api_manager.admin_steps.create_invalid_user(create_user_request)

        user_from_db = User.get_user_by_username(db_session, create_user_request.username)

        assert user_from_db is None, 'Пользователь создан, ошибка'


