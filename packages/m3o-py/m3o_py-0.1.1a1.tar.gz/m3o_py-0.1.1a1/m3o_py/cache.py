from typing import Union
from pydantic import BaseModel
from aiohttp import ClientSession
from m3o_py import GeneralException, UnknownError


class _DecrementReturn(BaseModel):
    key: str
    value: str


class _DeleteReturn(BaseModel):
    status: str


class _GetReturn(BaseModel):
    key: str
    ttl: int
    value: str


class _IncrementReturn(BaseModel):
    key: str
    value: int


class _ListKeysReturn(BaseModel):
    keys: list[str]


class _SetReturn(BaseModel):
    status: str


class CacheService:
    def __init__(self, token: str):
        self.token: str = token
        self.headers: dict = {"Authorization": f"Bearer {self.token}", "Content-Type": "application/json"}

    async def decrement(self, key: str, value: int) -> _DecrementReturn:
        async with ClientSession(headers=self.headers) as session:
            async with session.post("https://api.m3o.com/v1/cache/Decrement",
                                    json={"key": key, "value": value}) as resp:
                if resp.status == 500 or resp.status == 400:
                    raise GeneralException(await resp.json())
                elif resp.status == 200:
                    return _DecrementReturn(**await resp.json())
                else:
                    raise UnknownError(f"Unknown error: {resp.status}", await resp.json())

    async def delete(self, key: str) -> _DeleteReturn:
        async with ClientSession(headers=self.headers) as session:
            async with session.post("https://api.m3o.com/v1/cache/Delete",
                                    json={"key": key}) as resp:
                if resp.status == 500 or resp.status == 400:
                    raise GeneralException(await resp.json())
                elif resp.status == 200:
                    return _DeleteReturn(**await resp.json())
                else:
                    raise UnknownError(f"Unknown error: {resp.status}", await resp.json())

    async def get(self, key: str) -> _GetReturn | None:
        async with ClientSession(headers=self.headers) as session:
            async with session.post("https://api.m3o.com/v1/cache/Get",
                                    json={"key": key}) as resp:
                if resp.status == 500 or resp.status == 400:
                    raise GeneralException(await resp.json())
                elif resp.status == 200:
                    return _GetReturn(**await resp.json())
                else:
                    raise UnknownError(f"Unknown error: {resp.status}", await resp.json())

    async def increment(self, key: str, value: int) -> _IncrementReturn:
        async with ClientSession(headers=self.headers) as session:
            async with session.post("https://api.m3o.com/v1/cache/Increment",
                                    json={"key": key, "value": value}) as resp:
                if resp.status == 500 or resp.status == 400:
                    raise GeneralException(await resp.json())
                elif resp.status == 200:
                    return _IncrementReturn(**await resp.json())
                else:
                    raise UnknownError(f"Unknown error: {resp.status}", await resp.json())

    async def list_keys(self) -> _ListKeysReturn:
        async with ClientSession(headers=self.headers) as session:
            async with session.post("https://api.m3o.com/v1/cache/ListKeys") as resp:
                if resp.status == 500 or resp.status == 400:
                    raise GeneralException(await resp.json())
                elif resp.status == 200:
                    return _ListKeysReturn(**await resp.json())
                else:
                    raise UnknownError(f"Unknown error: {resp.status}", await resp.json())

    async def set(self, key: str, value: str, ttl: int) -> _SetReturn:
        async with ClientSession(headers=self.headers) as session:
            async with session.post("https://api.m3o.com/v1/cache/Set",
                                    json={"key": key, "value": value, "ttl": ttl}) as resp:
                if resp.status == 500 or resp.status == 400:
                    raise GeneralException(await resp.json())
                elif resp.status == 200:
                    return _SetReturn(**await resp.json())
                else:
                    raise UnknownError(f"Unknown error: {resp.status}", await resp.json())
