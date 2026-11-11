from http import HTTPStatus
from requests import Response
import requests

from src.main.api.models.repay_request import RepayRequest
from src.main.api.models.repay_response import RepayResponse
from src.main.api.requests.requester import Requester


class RepayRequester(Requester):
    def post(self, repay_request: RepayRequest) -> RepayResponse | Response:
        url=f'{self.base_url}/credit/repay'
        response = requests.post(
            url=url,
            json=repay_request.model_dump(),
            headers=self.headers
        )
        self.response_spec(response)
        if response.status_code in [HTTPStatus.OK]:
            return RepayResponse(**response.json())
        return response