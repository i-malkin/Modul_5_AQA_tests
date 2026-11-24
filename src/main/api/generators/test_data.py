
import random


# Диапазоны сумм из технического задания
DEPOSIT_MIN_AMOUNT = 1000
DEPOSIT_MAX_AMOUNT = 9000

TRANSFER_MIN_AMOUNT = 500
TRANSFER_MAX_AMOUNT = 10000

CREDIT_MIN_AMOUNT = 5000
CREDIT_MAX_AMOUNT = 15000


def generate_deposit_amount() -> float:
    """Генерирует случайную сумму пополнения."""
    return round(random.uniform(
        DEPOSIT_MIN_AMOUNT,
        DEPOSIT_MAX_AMOUNT
    ), 2)


def generate_transfer_amount(available_balance: float) -> float:
    """Генерирует сумму перевода с учетом баланса отправителя."""
    max_amount = min(TRANSFER_MAX_AMOUNT, available_balance)

    if max_amount < TRANSFER_MIN_AMOUNT:
        raise ValueError("Недостаточно средств для перевода")

    return round(random.uniform(
        TRANSFER_MIN_AMOUNT,
        max_amount
    ), 2)


def generate_credit_amount() -> float:
    """Генерирует случайную сумму кредита."""
    return float(random.randint(
        CREDIT_MIN_AMOUNT,
        CREDIT_MAX_AMOUNT
    ))
