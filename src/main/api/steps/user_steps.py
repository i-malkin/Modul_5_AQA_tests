from src.main.api.foundation.endpoint import Endpoint
from src.main.api.foundation.requesters.crud_requester import CrudRequester
from src.main.api.foundation.requesters.validate_crude_requester import ValidateCruseRequester
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.credit_request import CreditRequest
from src.main.api.models.deposit_request import DepositRequest
from src.main.api.models.repay_request import RepayRequest
from src.main.api.models.transfer_request import TransferRequest
from src.main.api.specs.request_specs import RequestSpecs
from src.main.api.specs.response_specs import ResponseSpecs
from src.main.api.steps.base_steps import BaseSteps


class UserSteps(BaseSteps):
    def create_account(self, create_user_request: CreateUserRequest):
        response = ValidateCruseRequester(
            RequestSpecs.auth_headers(username=create_user_request.username,
                                      password=create_user_request.password),
            Endpoint.CREATE_ACCOUNT,
            ResponseSpecs.request_created()
        ).post()
        return response

    def deposit(self, create_user_request: CreateUserRequest, deposit_request: DepositRequest):
        response = ValidateCruseRequester(
            RequestSpecs.auth_headers(username=create_user_request.username,
                                      password=create_user_request.password),
            Endpoint.DEPOSIT,
            ResponseSpecs.request_ok()
        ).post(deposit_request)
        return response

    def deposit_invalid(self, create_user_request: CreateUserRequest, deposit_request: DepositRequest):
        response = CrudRequester(
            RequestSpecs.auth_headers(username=create_user_request.username,
                                      password=create_user_request.password),
            Endpoint.DEPOSIT,
            ResponseSpecs.request_bad()
        ).post(deposit_request)
        return response

    def transfer(self, create_user_request: CreateUserRequest, transfer_request: TransferRequest):
        response = ValidateCruseRequester(
            RequestSpecs.auth_headers(username=create_user_request.username,
                                      password=create_user_request.password),
            Endpoint.TRANSFER,
            ResponseSpecs.request_ok()
        ).post(transfer_request)
        return response

    def transfer_invalid(self, create_user_request: CreateUserRequest, transfer_request: TransferRequest):
        response = CrudRequester(
            RequestSpecs.auth_headers(username=create_user_request.username,
                                      password=create_user_request.password),
            Endpoint.TRANSFER,
            ResponseSpecs.request_bad()
        ).post(transfer_request)
        return response

    def credit_request(self, create_user_request: CreateUserRequest, credit_request: CreditRequest):
        response = ValidateCruseRequester(
            RequestSpecs.auth_headers(username=create_user_request.username,
                                      password=create_user_request.password),
            Endpoint.CREDIT_REQUEST,
            ResponseSpecs.request_created()
        ).post(credit_request)
        return response

    def credit_request_invalid(self, create_user_request: CreateUserRequest, credit_request: CreditRequest):
        response = CrudRequester(
            RequestSpecs.auth_headers(username=create_user_request.username,
                                      password=create_user_request.password),
            Endpoint.CREDIT_REQUEST,
            ResponseSpecs.request_bad()
        ).post(credit_request)
        return response

    def credit_repay(self, create_user_request: CreateUserRequest, repay_request: RepayRequest):
        response = ValidateCruseRequester(
            RequestSpecs.auth_headers(username=create_user_request.username,
                                      password=create_user_request.password),
            Endpoint.CREDIT_REPAY,
            ResponseSpecs.request_ok()
        ).post(repay_request)
        return response

    def credit_repay_invalid(self, create_user_request: CreateUserRequest, repay_request: RepayRequest):
        response = CrudRequester(
            RequestSpecs.auth_headers(username=create_user_request.username,
                                      password=create_user_request.password),
            Endpoint.CREDIT_REPAY,
            ResponseSpecs.request_unprocessable()
        ).post(repay_request)
        return response