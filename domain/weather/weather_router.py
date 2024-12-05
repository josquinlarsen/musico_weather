from fastapi import APIRouter, HTTPException
import requests, os
from dotenv import load_dotenv
from domain.weather.weather_schema import WeatherAlert, WeatherResponse

router = APIRouter()

load_dotenv()

API_KEY = os.getenv("WEATHER_API_KEY")
if not API_KEY:
    raise Exception("API key not found. Please set it in the .env file.")
BASE_URL = "http://api.weatherapi.com/v1/current.json"

@router.get("/weather/{zipcode}", response_model=WeatherResponse)
async def get_weather(zipcode: str):
    url = f"{BASE_URL}?key={API_KEY}&q={zipcode}&aqi=no"
    response = requests.get(url)

    if response.status_code == 200:
        weather_data = response.json()
        curr_temp = weather_data["current"]["temp_f"]
        curr_precipitation = weather_data["current"]["precip_mm"]

        messages = weather_checks(curr_temp, curr_precipitation)

        return WeatherResponse(temperature=curr_temp, messages=[messages])

    else:
        raise HTTPException(status_code=500, detail="Error retrieving data. Try again.")


# ------------------------------------------------------------------
#       Utilities
# ------------------------------------------------------------------


def weather_checks(temperature, precipitation):
    """
    Checks conditions for temp range and precipitation
    """

    temp_message = ( 
        "Warning: Temperature is NOT within 60-75°F!"
        if temperature < 60 or temperature > 75
        else "Temperature is within 60-75°F range."
    )

    precip_message = (
        "Warning: Temperature is NOT within 60-75°F!"
        if precipitation > 0
        else "There is currently no precipitation."
    )

    return WeatherAlert(temp_message=temp_message, precip_message=precip_message)
