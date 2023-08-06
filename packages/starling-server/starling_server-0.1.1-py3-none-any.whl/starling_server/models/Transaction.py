from datetime import datetime
from typing import Optional

from pydantic.main import BaseModel

from starling_server.starling.models import StarlingTransaction
from starling_server.starling.utils import clean_string


class Transaction(BaseModel):
    """Represents a transaction."""

    uuid: str
    time: datetime
    counterparty_name: str
    amount: float
    reference: Optional[str] = None
    status: str

    @staticmethod
    def from_starling_transaction(other: StarlingTransaction) -> "Transaction":
        return Transaction(
            uuid=other.feedItemUid,
            time=other.transactionTime,
            counterparty_name=other.counterPartyName,
            amount=other.sourceAmount.compute_amount(other.direction),
            reference=clean_string(other.reference) if other.reference else None,
            status=other.status,
        )

    def __str__(self):
        return f"<TRANSACTION {self.time} {self.counterparty_name}:{self.amount}>"
