from pydantic import BaseModel


class WeatherAlert(BaseModel):
    temp_message: str
    precip_message: str


class WeatherResponse(BaseModel):
    temperature: float
    messages: list[WeatherAlert]
