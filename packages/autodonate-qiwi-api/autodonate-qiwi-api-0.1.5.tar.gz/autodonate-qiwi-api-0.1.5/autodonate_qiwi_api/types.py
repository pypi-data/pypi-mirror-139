from enum import Enum
from dataclasses import dataclass


class Operation(Enum):
    ALL = "ALL"
    IN = "IN"
    OUT = "OUT"
    QIWI_CARD = "QIWI_CARD"


class Source(Enum):
    RUB = "QW_RUB"
    USD = "QW_USD"
    EUR = "QW_EUR"
    CARD = "CARD"
    MK = "MK"


class Status:
    SUCCESS = 1


@dataclass
class Transaction:
    tx_id: int
    person_id: int
    date: str
    status = Status.SUCCESS
    type = Operation.IN
    account: str
    total: float
    commission: float
    amount: float
    comment: str = ""
