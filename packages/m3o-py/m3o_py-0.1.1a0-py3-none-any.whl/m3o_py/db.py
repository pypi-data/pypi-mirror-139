from typing import TypedDict, Union, Optional, Any
from aiohttp import ClientSession
from pydantic import BaseModel

from m3o_py import GeneralException, UnknownError


class _CountReturn(BaseModel):
    count: int


class _CreateReturn(BaseModel):
    id: str


class _ListTablesReturn(BaseModel):
    tables: list[str]


class _ReadReturn(BaseModel):
    records: list[dict[str, Any] | None]


class DbService:
    def __init__(self, token: str):
        self.token: str = token
        self.headers: dict = {"Authorization": f"Bearer {self.token}", "Content-Type": "application/json"}

    async def count(self, table: str) -> _CountReturn:
        async with ClientSession() as session:
            async with session.post("https://api.m3o.com/v1/db/Count", headers=self.headers,
                                    json={"table": table}) as resp:
                if resp.status == 500 or resp.status == 400:
                    raise GeneralException(await resp.json())
                elif resp.status == 200:
                    return _CountReturn(**await resp.json())
                else:
                    raise UnknownError(f"Unknown error: {resp.status}", await resp.json())

    async def create(self, table: str, record: dict) -> _CreateReturn:
        """

        :param table: The table where the data should be stored
        :param record: The actual data to be stored
        :return: The id of the record
        """
        async with ClientSession() as session:
            async with session.post("https://api.m3o.com/v1/db/Create", headers=self.headers,
                                    json={"table": table, "record": record}) as resp:
                if resp.status == 500 or resp.status == 400:
                    raise GeneralException(await resp.json())
                elif resp.status == 200:
                    return _CreateReturn(**await resp.json())
                else:
                    raise UnknownError(f"Unknown error: {resp.status}", await resp.json())

    async def delete(self, table: str, id: str) -> None:
        """
        :param table: The table where the data should be stored
        :param id: The id pf the element to be deleted
        :return: None
        """
        async with ClientSession() as session:
            async with session.post("https://api.m3o.com/v1/db/Delete", headers=self.headers,
                                    json={"table": table, "id": id}) as resp:
                if resp.status == 500 or resp.status == 400:
                    raise GeneralException(await resp.json())
                elif resp.status == 200:
                    return
                else:
                    raise UnknownError(f"Unknown error: {resp.status}", await resp.json())

    async def drop_table(self, table: str) -> None:
        """
        :param table: The table to be dropped
        :return: None
        """
        async with ClientSession() as session:
            async with session.post("https://api.m3o.com/v1/db/DropTable", headers=self.headers,
                                    json={"table": table}) as resp:
                if resp.status == 500 or resp.status == 400:
                    raise GeneralException(await resp.json())
                elif resp.status == 200:
                    return
                else:
                    raise UnknownError(f"Unknown error: {resp.status}", await resp.json())

    async def list_tables(self) -> _ListTablesReturn:
        """
        :return: None
        """
        async with ClientSession() as session:
            async with session.post("https://api.m3o.com/v1/db/ListTables", headers=self.headers) as resp:
                if resp.status == 500 or resp.status == 400:
                    raise GeneralException(await resp.json())
                elif resp.status == 200:
                    return _ListTablesReturn(**await resp.json())
                else:
                    raise UnknownError(f"Unknown error: {resp.status}", await resp.json())

    async def read(self, id: Optional[str] = None,
                   limit: Optional[int] = None,
                   offest: Optional[str] = None,
                   order: Optional[str] = None,
                   orderBy: Optional[str] = None,
                   query: str = None,
                   table: str = None) -> _ReadReturn:
        async with ClientSession() as session:
            async with session.post("https://api.m3o.com/v1/db/Read", headers=self.headers,
                                    json={"id": id, "limit": limit, "offset": offest, "order": order,
                                          "orderBy": orderBy, "query": query, "table": table}) as resp:
                if resp.status == 500 or resp.status == 400:
                    raise GeneralException(await resp.json())
                elif resp.status == 200:
                    return _ReadReturn(**await resp.json())
                else:
                    raise UnknownError(f"Unknown error: {resp.status}", await resp.json())

    async def rename_table(self, from_table: str, to: str) -> None:
        async with ClientSession() as session:
            async with session.post("https://api.m3o.com/v1/db/RenameTable", headers=self.headers,
                                    json={"from": from_table, "to": to}) as resp:
                if resp.status == 500 or resp.status == 400:
                    raise GeneralException(await resp.json())
                elif resp.status == 200:
                    return
                else:
                    raise UnknownError(f"Unknown error: {resp.status}", await resp.json())

    async def truncate(self, table: str) -> None:
        async with ClientSession() as session:
            async with session.post("https://api.m3o.com/v1/db/Truncate", headers=self.headers,
                                    json={"table": table}) as resp:
                if resp.status == 500 or resp.status == 400:
                    raise GeneralException(await resp.json())
                elif resp.status == 200:
                    return
                else:
                    raise UnknownError(f"Unknown error: {resp.status}", await resp.json())

    async def update(self, table: str, id: str, data: dict[str, Any]) -> None:
        """
        :param table: Table name. Defaults to 'default'
        :param id: The id of the record. Will overwrite if id is set in data
        :param data: The data to be updated
        :return:
        """
        async with ClientSession() as session:
            async with session.post("https://api.m3o.com/v1/db/Update", headers=self.headers,
                                    json={"table": table, "record": data, "id": id}) as resp:
                if resp.status == 500 or resp.status == 400:
                    raise GeneralException(await resp.json())
                elif resp.status == 200:
                    return
                else:
                    raise UnknownError(f"Unknown error: {resp.status}", await resp.json())
