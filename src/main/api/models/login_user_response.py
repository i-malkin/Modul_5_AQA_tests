from src.main.api.models.base_model import BaseModel

class User(BaseModel):
    username: str
    password: str

class LoginUserResponse(BaseModel):
    token: str
    user: User

