from datetime import datetime
from typing import List

from pydantic.main import BaseModel


class StarlingAccount(BaseModel):
    """Represents a Starling Account."""
    accountUid: str
    accountType: str
    defaultCategory: str
    currency: str
    createdAt: datetime
    name: str


class AccountsResponse(BaseModel):
    accounts: List[StarlingAccount]
