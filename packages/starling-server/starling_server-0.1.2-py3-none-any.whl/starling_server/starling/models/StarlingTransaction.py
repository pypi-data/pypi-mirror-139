# Transaction.py
# Richard Lyon, 20 February 2022
from datetime import datetime
from typing import Optional, List

from pydantic.main import BaseModel


class SourceAmount(BaseModel):
    """Currency dcit"""

    currency: str
    minorUnits: int

    def compute_amount(self, direction: str) -> float:
        """Compute a transaction amount in pounds. Outflow is negative."""
        if direction == "OUT":
            sign = -1
        else:
            sign = 1

        return sign * self.minorUnits / 100.0


class StarlingTransaction(BaseModel):
    """Response from the starling api"""

    feedItemUid: str
    transactionTime: datetime
    counterPartyName: str
    direction: str
    sourceAmount: SourceAmount
    reference: Optional[str] = None
    status: str


class FeedItemsResponse(BaseModel):
    feedItems: List[StarlingTransaction]
