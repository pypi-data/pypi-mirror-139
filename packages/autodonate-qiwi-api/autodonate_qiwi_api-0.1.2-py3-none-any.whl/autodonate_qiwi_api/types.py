from enum import Enum
from dataclasses import dataclass


class Operation(Enum):
    ALL = 0
    IN = 1
    OUT = 2
    QIWI_CARD = 3


class Source(Enum):
    RUB = 0
    USD = 1
    EUR = 2


class SourceCard(Enum):
    CARD = 0


class SourceMK(Enum):
    MK = 0


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
