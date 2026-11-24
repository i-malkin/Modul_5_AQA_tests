import requests
from typing import Dict
from src.main.api.models.login_user_request import LoginUserRequest
from src.main.api.models.login_user_response import LoginUserResponse


class RequestSpecs:
    @staticmethod
    def base_headers() -> Dict[str, str]:
        return {
            "Content-Type": "application/json",
            "accept": "application/json"
        }

    @staticmethod
    def auth_headers(username: str, password: str) -> Dict[str, str]:
        request = LoginUserRequest(username=username, password=password)
        response = requests.post(
            url="http://localhost:4111/api/auth/token/login",
            json=request.model_dump(),
            headers=RequestSpecs.base_headers(),
        )
        if response.status_code == 200:
            response_data = LoginUserResponse(**response.json())
            token = response_data.token
            headers = RequestSpecs.base_headers()
            headers["Authorization"] = f"Bearer {token}"
            return headers
        raise Exception("Failed to authenticate")

    @staticmethod
    def unauth_headers() -> Dict[str, str]:
        return RequestSpecs.base_headers()

