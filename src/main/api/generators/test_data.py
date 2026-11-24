import random

DEPOSIT_MIN_AMOUNT = 1000
DEPOSIT_MAX_AMOUNT = 9000

TRANSFER_MIN_AMOUNT = 500
TRANSFER_MAX_AMOUNT = 10000

CREDIT_MIN_AMOUNT = 5000
CREDIT_MAX_AMOUNT = 15000

def generate_deposit_amount() -> float:
    return round(random.uniform(
        DEPOSIT_MIN_AMOUNT,
        DEPOSIT_MAX_AMOUNT
    ), 2)

def generate_transfer_amount(available_balance: float) -> float:
    max_amount = min(TRANSFER_MAX_AMOUNT, available_balance)

    if max_amount < TRANSFER_MIN_AMOUNT:
        raise ValueError("Недостаточно средств для перевода")

    return round(random.uniform(
        TRANSFER_MIN_AMOUNT,
        max_amount
    ), 2)


def generate_credit_amount() -> float:
    return float(random.randint(
        CREDIT_MIN_AMOUNT,
        CREDIT_MAX_AMOUNT
    ))


CREDIT_TERM_MONTHS = 12
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "123456"

DEPOSIT_RANGE_ERROR = f"Amount must be between {DEPOSIT_MIN_AMOUNT} and {DEPOSIT_MAX_AMOUNT}"
TRANSFER_RANGE_ERROR = f"Amount must be between {TRANSFER_MIN_AMOUNT} and {TRANSFER_MAX_AMOUNT}"
TRANSFER_POSITIVE_ERROR = "Amount must be greater than 0"
CREDIT_RANGE_ERROR = f"Amount must be between {CREDIT_MIN_AMOUNT} and {CREDIT_MAX_AMOUNT}"


def generate_negative_amount() -> int:
    return -random.randint(1, 1000)

def invalid_deposit_amounts() -> list[float]:
    return [generate_negative_amount(), 0, DEPOSIT_MIN_AMOUNT - 1, DEPOSIT_MAX_AMOUNT + 1]

def invalid_credit_amounts() -> list[float]:
    return [generate_negative_amount(), 0, CREDIT_MIN_AMOUNT - 1, CREDIT_MAX_AMOUNT + 1]

def invalid_transfer_cases() -> list[tuple[float, str]]:
    return [
        (generate_negative_amount(), TRANSFER_POSITIVE_ERROR),
        (0, TRANSFER_POSITIVE_ERROR),
        (TRANSFER_MIN_AMOUNT - 1, TRANSFER_RANGE_ERROR),
        (TRANSFER_MAX_AMOUNT + 1, TRANSFER_RANGE_ERROR),
    ]
