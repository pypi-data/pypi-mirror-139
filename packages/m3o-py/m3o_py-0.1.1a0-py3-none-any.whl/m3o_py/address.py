from typing import TypedDict, Optional
from aiohttp import ClientSession
from pydantic import BaseModel

from m3o_py import GeneralException, UnknownError


class _AddressReturn(BaseModel):
    line_one: str
    line_two: str
    summary: Optional[str]
    organisation: Optional[str]
    building_name: Optional[str]
    premise: Optional[str]
    street: str
    locality: Optional[str]
    town: Optional[str]
    county: Optional[str]
    postcode: str


class _AddressReturnWrapper(BaseModel):
    addresses: list[_AddressReturn]


class AddressService:
    def __init__(self, token: str):
        self.token: str = token
        self.headers: dict = {"Authorization": f"Bearer {self.token}", "Content-Type": "application/json"}

    async def lookup_postcode(self, postcode: str) -> _AddressReturnWrapper:
        async with ClientSession() as session:
            async with session.post("https://api.m3o.com/v1/address/LookupPostcode", json={"postcode": postcode},
                                    headers=self.headers) as resp:
                if resp.status == 500 or resp.status == 400:
                    raise GeneralException(await resp.json())
                elif resp.status == 200:
                    return _AddressReturnWrapper(**await resp.json())
                else:
                    raise UnknownError(f"Unknown error: {resp.status}", await resp.json())
