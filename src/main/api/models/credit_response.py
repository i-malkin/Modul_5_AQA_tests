from src.main.api.models.base_model import BaseModel


class CreditResponse(BaseModel):
    id: int  # это id счёта
    amount: float
    termMonths: int
    balance: float
    creditId: int

