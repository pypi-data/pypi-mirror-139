from typing import TypedDict, Optional
from aiohttp import ClientSession
from pydantic import BaseModel

from m3o_py import GeneralException, UnknownError


class _LookupReturn(BaseModel):
    asn: int
    city: str
    continent: str
    country: str
    ip: str
    latitude: float
    longitude: float
    timezone: str


class IP2GeoService:
    def __init__(self, token: str):
        self.token: str = token
        self.headers: dict = {"Authorization": f"Bearer {self.token}", "Content-Type": "application/json"}

    async def lookup(self, ip: str) -> _LookupReturn:
        async with ClientSession() as session:
            async with session.post("https://api.m3o.com/v1/ip/Lookup", json={"ip": ip}, headers=self.headers) as resp:
                if resp.status == 500 or resp.status == 400:
                    raise GeneralException(await resp.json())
                elif resp.status == 200:
                    return _LookupReturn(**await resp.json())
                else:
                    raise UnknownError(f"Unknown error: {resp.status}", await resp.json())
