from src.main.api.generators.creations_rule import CreationsRule
from src.main.api.models.base_model import BaseModel
from typing import Annotated



class CreateUserRequest(BaseModel):
    username: Annotated[str, CreationsRule(regex=r'^[A-Za-z0-9]{3,15}$')]
    password: Annotated[str, CreationsRule(regex=r'^[A-Z]{3}[a-z]{1}[0-9]{2}[!$_]{4}$')]
    role: Annotated[str, CreationsRule(regex=r'^ROLE_USER')]



