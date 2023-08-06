from typing import List, Optional

from fastapi import FastAPI

from starling_server.config import get_token_account__from_name
from starling_server.models import Transaction, Account
from starling_server.starling.api import api_get_accounts, api_get_balance_for_account_uid, \
    api_get_settled_transactions_for_account_days

app = FastAPI()


# Accounts #############################################################################


@app.get("/accounts/{name}", tags=["Accounts"], response_model=List[Account])
async def get_accounts(name: str) -> List[Account]:
    token, _ = get_token_account__from_name(name)
    data = await api_get_accounts(token)
    return [Account.from_starling_account(d, token) for d in data.accounts]


@app.get("/account/{name}/balance", tags=["Accounts"], response_model=Optional[float])
async def get_account_balance(name: str) -> Optional[float]:
    token, account_uid = get_token_account__from_name(name)
    return await api_get_balance_for_account_uid(token, account_uid)


# Transactions #############################################################################


@app.get("/account/{name}/transactions", tags=["Transactions"], response_model=List[Transaction])
async def get_settled_transactions_for_account(name: str) -> List[Transaction]:
    return await get_settled_transactions_for_account_days(name, 7)


@app.get(
    "/account/{name}/transactions/{days}",
    tags=["Transactions"],
    response_model=List[Transaction],
)
async def get_settled_transactions_for_account_days(
        name: str, days: int
) -> List[Transaction]:
    token, account_uid = get_token_account__from_name(name)
    return await api_get_settled_transactions_for_account_days(token, account_uid, days)
