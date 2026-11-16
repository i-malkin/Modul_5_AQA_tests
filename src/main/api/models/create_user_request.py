from src.main.api.generators.creations_rule import CreationsRule
from src.main.api.models.base_model import BaseModel
from typing import Annotated
from enum import Enum

class UserRole(str, Enum):
    USER = "ROLE_USER"
    CREDIT_SECRET = "ROLE_CREDIT_SECRET"
    ADMIN = "ROLE_ADMIN"


class CreateUserRequest(BaseModel):
    username: Annotated[str, CreationsRule(regex=r'^[A-Za-z0-9]{3,15}$')]
    password: Annotated[str, CreationsRule(regex=r'^[A-Z]{3}[a-z]{1}[0-9]{2}[!$_]{4}$')]
    role: UserRole = UserRole.USER



