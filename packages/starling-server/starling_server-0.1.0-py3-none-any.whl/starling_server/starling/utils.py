import re
from typing import TypeVar, Type, Any

import httpx
from pydantic import parse_obj_as

T = TypeVar("T")


async def get(
        token: str, path: str, params: dict = None, return_type: Type[T] = Any
) -> T:
    """Get an api call."""
    API_BASE_URL = "https://api.starlingbank.com/api/v2"

    headers = {"Authorization": f"Bearer {token}", "User-Agent": "python"}
    url = f"{API_BASE_URL}{path}"

    async with httpx.AsyncClient() as client:
        try:
            r = await client.get(url, headers=headers, params=params)
            r.raise_for_status()
        except httpx.HTTPError as e:
            raise Exception(e)

        if return_type is not None:
            return parse_obj_as(return_type, r.json())
        else:
            return r.json()


def clean_string(the_string: str) -> str:
    """Replace multiple spaces with a single space."""
    try:
        return re.sub(" +", " ", the_string)

    except:
        return the_string
