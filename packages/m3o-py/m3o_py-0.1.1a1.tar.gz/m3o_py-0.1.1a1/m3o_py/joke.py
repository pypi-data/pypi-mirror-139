from typing import TypedDict, Optional
from aiohttp import ClientSession
from pydantic import BaseModel

from m3o_py import GeneralException, UnknownError


class _JokeResponse(BaseModel):
    """
    Response from the Joke API.
    """
    id: str
    title: str
    body: str
    category: str
    source: str


class _JokeResponseReturn(BaseModel):
    jokes: list[_JokeResponse | None]


class JokeService:
    def __init__(self, token: str):
        self.token: str = token
        self.headers: dict = {"Authorization": f"Bearer {self.token}", "Content-Type": "application/json"}

    async def random(self, count: int = 1) -> _JokeResponseReturn:
        async with ClientSession() as session:
            async with session.post("https://api.m3o.com/v1/joke/Random", json={"count": count},
                                    headers=self.headers) as resp:
                if resp.status == 500 or resp.status == 400:
                    raise GeneralException(await resp.json())
                elif resp.status == 200:
                    return _JokeResponseReturn(**await resp.json())
                else:
                    raise UnknownError(f"Unknown error: {resp.status}", await resp.json())
