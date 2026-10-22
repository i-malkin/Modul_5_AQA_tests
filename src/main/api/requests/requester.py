from abc import ABC, abstractmethod
from typing import Dict, Callable
from src.main.api.models.base_model import BaseModel

class Requester(ABC):
    def __init__(self, request_spect: Dict[str, str], response_spec: Callable):
        self.headers = request_spect["headers"]
        self.base_url = request_spect["base_url"]
        self.response_spec = response_spec

    @abstractmethod
    def post(self, model: BaseModel): ...
