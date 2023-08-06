from datetime import datetime

from pydantic.main import BaseModel

from starling_server.starling.models import StarlingAccount


class Account(BaseModel):
    """Represents an Account."""

    token: str
    uuid: str
    type: str
    default_category: str
    currency: str
    created: datetime
    name: str

    @staticmethod
    def from_starling_account(data: StarlingAccount, token: str) -> "Account":
        return Account(
            token=token,
            uuid=data.accountUid,
            type=data.accountType,
            default_category=data.defaultCategory,
            currency=data.currency,
            created=data.createdAt,
            name=data.name,
        )

    def __str__(self):
        return f"<ACCOUNT: {self.name} {self.uuid}>"
