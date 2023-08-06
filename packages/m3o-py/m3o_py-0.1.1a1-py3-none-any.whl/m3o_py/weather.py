from m3o_py import GeneralException, UnknownError
from aiohttp import ClientSession
from pydantic import BaseModel


class _ForecastEntry(BaseModel):
    date: str
    max_temp_c: float
    max_temp_f: float
    min_temp_c: float
    min_temp_f: float
    avg_temp_c: float
    avg_temp_f: float
    condition: str
    icon_url: str
    sunrise: str
    sunset: str
    max_wind_mph: float
    max_wind_kph: float


class _ForecastResponse(BaseModel):
    forecast: list[_ForecastEntry]
    location: str
    region: str
    country: str
    latitude: float
    longitude: float
    timezone: str
    local_time: str


class _NowResponse(BaseModel):
    location: str
    region: str
    country: str
    latitude: float
    longitude: float
    timezone: str
    local_time: str
    temp_c: float
    temp_f: float
    feels_like_c: float
    feels_like_f: float
    humidity: float
    cloud: float
    daytime: bool
    condition: str
    icon_url: str
    wind_mph: float
    wind_kph: float
    wind_direction: str
    wind_degree: float


class WeatherService:
    def __init__(self, token: str):
        self.token: str = token
        self.headers: dict = {"Authorization": f"Bearer {self.token}", "Content-Type": "application/json"}

    async def forecast(self, location: str, days: int = 1) -> _ForecastResponse:
        async with ClientSession() as session:
            async with session.post("https://api.m3o.com/v1/weather/Forecast",
                                    json={"location": location, "days": days}, headers=self.headers) as resp:
                if resp.status == 500:
                    raise GeneralException(await resp.json())
                elif resp.status == 200:
                    print(await resp.json())
                    return _ForecastResponse(**await resp.json())
                else:
                    raise UnknownError(f"Unknown error: {resp.status}", await resp.json())

    async def now(self, location: str) -> _NowResponse:
        async with ClientSession() as session:
            async with session.post("https://api.m3o.com/v1/weather/Now",
                                    json={"location": location}, headers=self.headers) as resp:
                if resp.status == 500:
                    raise GeneralException(await resp.json())
                elif resp.status == 200:
                    print(await resp.json())
                    return _NowResponse(**await resp.json())
                else:
                    raise UnknownError(f"Unknown error: {resp.status}", await resp.json())
