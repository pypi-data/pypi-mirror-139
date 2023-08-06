from typing import TypedDict, Optional
from aiohttp import ClientSession
from pydantic import BaseModel

from m3o_py import GeneralException, UnknownError


class _Tweet(BaseModel):
    id: str
    text: str
    username: str
    created_at: str
    retweeted_count: str
    favourited_count: str


class _SearchResponse(BaseModel):
    tweets: list[_Tweet | None]


class _Trend(BaseModel):
    name: str
    url: str
    tweet_volume: str


class _TrendsResponse(BaseModel):
    trends: list[_Trend]


class _Profile(BaseModel):
    id: str
    name: Optional[str]
    username: str
    description: Optional[str]
    created_at: str
    location: Optional[str]
    followers: str
    private: bool
    verified: bool
    image_url: str


class _Status(BaseModel):
    id: str
    text: str
    username: str
    created_at: str
    retweeted_count: str
    favourited_count: str


class _UserResponse(BaseModel):
    status: _Status
    profile: _Profile


class TwitterService:
    def __init__(self, token: str):
        self.token: str = token
        self.headers: dict = {"Authorization": f"Bearer {self.token}", "Content-Type": "application/json"}

    async def search(self, query: str, limit: int = 20) -> _SearchResponse:
        async with ClientSession() as session:
            async with session.post("https://api.m3o.com/v1/twitter/Search", json={"query": query, "limit": limit},
                                    headers=self.headers) as resp:
                if resp.status == 500 or resp.status == 400:
                    raise GeneralException(await resp.json())
                elif resp.status == 200:
                    return _SearchResponse(**await resp.json())
                else:
                    raise UnknownError(f"Unknown error: {resp.status}", await resp.json())

    async def timeline(self, username: str, limit: int = 20) -> _SearchResponse:
        async with ClientSession() as session:
            async with session.post("https://api.m3o.com/v1/twitter/Timeline", json={"username": username,
                                                                                     "limit": limit},
                                    headers=self.headers) as resp:
                if resp.status == 500 or resp.status == 400:
                    raise GeneralException(await resp.json())
                elif resp.status == 200:
                    return _SearchResponse(**await resp.json())
                else:
                    raise UnknownError(f"Unknown error: {resp.status}", await resp.json())

    async def trends(self) -> _TrendsResponse:
        async with ClientSession() as session:
            async with session.post("https://api.m3o.com/v1/twitter/Trends", headers=self.headers) as resp:
                if resp.status == 500 or resp.status == 400:
                    raise GeneralException(await resp.json())
                elif resp.status == 200:
                    return _TrendsResponse(**await resp.json())
                else:
                    raise UnknownError(f"Unknown error: {resp.status}", await resp.json())

    async def user(self, username: str) -> _UserResponse:
        async with ClientSession() as session:
            async with session.post("https://api.m3o.com/v1/twitter/User", json={"username": username},
                                    headers=self.headers) as resp:
                if resp.status == 500 or resp.status == 400:
                    raise GeneralException(await resp.json())
                elif resp.status == 200:
                    return _UserResponse(**await resp.json())
                else:
                    raise UnknownError(f"Unknown error: {resp.status}", await resp.json())
