from pydantic import BaseModel


class WeatherAlert(BaseModel):
    alert_message: str


class WeatherResponse(BaseModel):
    temperature: float
    messages: list[WeatherAlert]
