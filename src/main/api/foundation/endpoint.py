from src.main.api.models.base_model import BaseModel
from typing import Optional, Type
from dataclasses import dataclass
from enum import Enum
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.create_user_response import CreateUserResponse


@dataclass()
class EndpointConfiguration:
    url: str
    request_model: Optional[Type[BaseModel]]
    response_model: Optional[Type[BaseModel]]


class Endpoint(Enum):
    ADMIN_CREATE_USER = EndpointConfiguration(
        request_model=CreateUserRequest,
        url="/account/create",
        response_model=CreateUserResponse
    )

    ADMIN_DELETE_USER =EndpointConfiguration(
        request_model=None,
        url="/admin/users",
        response_model=None
    )



