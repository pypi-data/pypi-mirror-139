from typing import TypedDict, Union
from aiohttp import ClientSession
from pydantic import BaseModel
from m3o_py import GeneralException, UnknownError


class QuestionResponse(BaseModel):
    answer: str
    url: str
    image: str


class AnswerService:
    def __init__(self, token: str):
        self.token: str = token
        self.headers: dict = {"Authorization": f"Bearer {self.token}", "Content-Type": "application/json"}

    async def question(self, query: str) -> QuestionResponse | UnknownError | GeneralException:
        async with ClientSession() as session:
            async with session.post("https://api.m3o.com/v1/answer/Question", json={"query": query},
                                    headers=self.headers) as resp:
                if resp.status == 500 or resp.status == 400:
                    raise GeneralException(await resp.json())
                elif resp.status == 200:
                    return QuestionResponse(**await resp.json())
                else:
                    raise UnknownError(f"Unknown error: {resp.status}", await resp.json())
