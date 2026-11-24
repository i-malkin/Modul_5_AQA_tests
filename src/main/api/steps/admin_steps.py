from src.main.api.generators.test_data import ADMIN_USERNAME, ADMIN_PASSWORD
from src.main.api.models.create_user_response import CreateUserResponse
from src.main.api.models.login_user_response import LoginUserResponse
from src.main.api.foundation.endpoint import Endpoint
from src.main.api.foundation.requesters.crud_requester import CrudRequester
from src.main.api.foundation.requesters.validate_crude_requester import ValidateCruseRequester
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.login_user_request import LoginUserRequest
from src.main.api.specs.request_specs import RequestSpecs
from src.main.api.specs.response_specs import ResponseSpecs
from src.main.api.steps.base_steps import BaseSteps


class AdminSteps(BaseSteps):
    def create_user(self, create_user_request: CreateUserRequest) -> CreateUserResponse:
        response = ValidateCruseRequester(
            RequestSpecs.auth_headers(username=ADMIN_USERNAME, password=ADMIN_PASSWORD),
            Endpoint.ADMIN_CREATE_USER,
            ResponseSpecs.request_ok()
        ).post(create_user_request)

        self.created_obj.append(response)
        return response

    def delete_user(self, user_id: int) -> None:
        CrudRequester(
            RequestSpecs.auth_headers(username=ADMIN_USERNAME, password=ADMIN_PASSWORD),
            Endpoint.ADMIN_DELETE_USER,
            ResponseSpecs.request_ok()
        ).delete(user_id)


    def create_invalid_user(self, create_user_request: CreateUserRequest) -> None:
        CrudRequester(
            RequestSpecs.auth_headers(username=ADMIN_USERNAME, password=ADMIN_PASSWORD),
            Endpoint.ADMIN_CREATE_USER,
            ResponseSpecs.request_bad()
        ).post(create_user_request)


    def login_user(self, login_user_request: LoginUserRequest) -> LoginUserResponse:
        response = ValidateCruseRequester(
            RequestSpecs.unauth_headers(),
            Endpoint.LOGIN_USER,
            ResponseSpecs.request_ok()
        ).post(login_user_request)
        return response

