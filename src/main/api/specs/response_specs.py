from requests import Response
from http import HTTPStatus
from typing import Callable


class ResponseSpecs:
    @staticmethod
    def request_ok() -> Callable[[Response], None]:
        def confirm(response: Response) -> None:
            assert response.status_code == HTTPStatus.OK, response.text
        return confirm

    @staticmethod
    def request_created() -> Callable[[Response], None]:
        def confirm(response: Response) -> None:
            assert response.status_code == HTTPStatus.CREATED, response.text
        return confirm

    @staticmethod
    def request_bad() -> Callable[[Response], None]:
        def confirm(response: Response) -> None:
            assert response.status_code == HTTPStatus.BAD_REQUEST, response.text
        return confirm

    @staticmethod
    def request_unprocessable() -> Callable[[Response], None]:
        def confirm(response: Response) -> None:
            assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY, response.text
        return confirm

