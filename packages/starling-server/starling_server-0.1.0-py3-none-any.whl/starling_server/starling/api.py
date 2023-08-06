from datetime import datetime, timedelta
from typing import Optional, List
from urllib.error import HTTPError

from pydantic import PydanticTypeError

from starling_server.models import Transaction
from starling_server.starling.models.StarlingAccount import AccountsResponse
from starling_server.starling.models.StarlingTransaction import FeedItemsResponse
from starling_server.starling.utils import get


async def api_get_accounts(token: str) -> AccountsResponse:
    return await get(token, "/accounts", None, AccountsResponse)


async def api_get_balance_for_account_uid(token: str, account_uid: str) -> Optional[float]:
    path = f"/accounts/{account_uid}/balance"
    data: dict = await get(token, path, None, dict)

    balance = data.get("clearedBalance")
    if balance is not None:
        minor_units = balance.get("minorUnits")

        if minor_units is not None:
            return minor_units / 100.0

    return None


async def api_get_settled_transactions_for_account_days(token: str, account_uid: str, days: int) -> List[Transaction]:
    max_transaction_timestamp = datetime.now()
    min_transaction_timestamp = max_transaction_timestamp - timedelta(days=days)

    path = f"/feed/account/{account_uid}/settled-transactions-between"
    params = {
        "minTransactionTimestamp": min_transaction_timestamp.strftime(
            "%Y-%m-%dT00:00:00.000Z"
        ),
        "maxTransactionTimestamp": max_transaction_timestamp.strftime(
            "%Y-%m-%dT00:00:00.000Z"
        ),
    }

    try:
        data = await get(token, path, params, FeedItemsResponse)

    except HTTPError:
        raise RuntimeError(f"failed to get transactions for Starling account '{name}'")
    except PydanticTypeError:
        raise RuntimeError(f"")

    return [Transaction.from_starling_transaction(item) for item in data.feedItems]
