from fastapi import APIRouter, HTTPException
import requests
from weather_schema import WeatherAlert, WeatherResponse
from main import API_KEY, BASE_URL

router = APIRouter()

@router.get("/weather/{zipcode}", response_model=WeatherResponse)
async def get_weather(zipcode: str):
    url = f"{BASE_URL}?key={API_KEY}&q={zipcode}&aqi=no"
    response = requests.get(url)

    if response.status_code == 200:
        weather_data = response.json()
        curr_temp = weather_data["current"]["temp_f"]
        curr_precipitation = weather_data["current"]["precip_mm"]

        messages = weather_checks(curr_temp, curr_precipitation)

        return WeatherResponse(temperature=curr_temp, messages=messages)

    else:
        raise HTTPException(status_code=500, detail="Error retrieving data. Try again.")

# ------------------------------------------------------------------
#       Utilities
# ------------------------------------------------------------------


def weather_checks(temperature, precipitation):
    """
    Checks conditions for temp range and precipitation
    """

    messages = []

    if 60 < temperature > 75:
        messages.append(
            WeatherAlert(temp_message="Warning: Temperature is NOT within 60-75°F!")
        )
    else:
        messages.append(
            WeatherAlert(temp_message="Temperature is within 60-75°F range.")
        )

    if precipitation > 0:
        messages.append(WeatherAlert(precip_message="Warning: There is precipitation!"))
    else:
        messages.append(
            WeatherAlert(precip_message="There is currently no precipitation.")
        )

    return messages
