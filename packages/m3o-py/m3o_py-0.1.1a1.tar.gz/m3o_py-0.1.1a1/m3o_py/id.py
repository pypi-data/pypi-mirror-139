from typing import TypedDict, Optional
from aiohttp import ClientSession
from pydantic import BaseModel

from m3o_py import GeneralException, UnknownError


class _GenerateReturn(BaseModel):
    id: str
    type: str


class _TypesReturn(BaseModel):
    types: list[str]


class IDgenService:
    def __init__(self, token: str):
        self.token: str = token
        self.headers: dict = {"Authorization": f"Bearer {self.token}", "Content-Type": "application/json"}

    async def generate(self, type: str) -> _GenerateReturn:
        async with ClientSession() as session:
            async with session.post("https://api.m3o.com/v1/id/Generate", json={"type": type},
                                    headers=self.headers) as resp:
                if resp.status == 500 or resp.status == 400:
                    raise GeneralException(await resp.json())
                elif resp.status == 200:
                    return _GenerateReturn(**await resp.json())
                else:
                    raise UnknownError(f"Unknown error: {resp.status}", await resp.json())

    async def types(self) -> _TypesReturn:
        async with ClientSession() as session:
            async with session.post("https://api.m3o.com/v1/id/Types", headers=self.headers, json={}) as resp:
                if resp.status == 500 or resp.status == 400:
                    raise GeneralException(await resp.json())
                elif resp.status == 200:
                    return _TypesReturn(**await resp.json())
                else:
                    raise UnknownError(f"Unknown error: {resp.status}", await resp.json())
